#!/usr/bin/python
import connect
import time
# ----------BEGIN : USER CONFIG VARIABLE SECTION----------

fmc_hostname = "fmc"
fmc_username = "admin"
fmc_password = "password"
domain = "Global"

number_of_bulk_rules = 10
number_of_non_bulk_rules = 10
number_of_ACLs = 100

# ----------END : USER CONFIG VARIABLE SECTION----------


print("Connecting to FMC")
fmc = connect.fmc(fmc_hostname, fmc_username, fmc_password)
fmc.tokenGeneration(domain)

access_policy = {
  "type": "AccessPolicy",
  "name": "BULK-ACP",
  "defaultAction": {
    "action": "BLOCK"
  }
}

small_access_policy = {
  "type": "AccessPolicy",
  "name": "NON-BULK-ACP",
  "defaultAction": {
    "action": "BLOCK"
  }
}

print("Creating BULK-ACP Access Control Policy ")
policy_id = fmc.createPolicy(access_policy)

print("Creating NON-BULK-ACP Access Control Policy ")
small_policy_id = fmc.createPolicy(small_access_policy)


#
# Bulk method
#
print(f"Creating {number_of_bulk_rules*number_of_ACLs} ACLs with bulk method")


bulk_rules = []

while number_of_bulk_rules > 0:
    for num in range(1, number_of_ACLs+1):
        network = "1.1."+str(number_of_bulk_rules)+"."+str(num)
        access_rule = {
            "action": "ALLOW",
            "enabled": True,
            "type": "AccessRule",
            "sendEventsToFMC": True,
            "vlanTags": {},
            "sourceNetworks": {
                "literals": [
                  {
                    "type": "Network",
                    "value": network
                  }
                ]
            },
            "logBegin": False,
            "logEnd": True,
            "logFiles": False,
            "name": network + "-to-any"
        }
        bulk_rules.append(access_rule)
    number_of_bulk_rules = number_of_bulk_rules - 1


start_time = time.time()
fmc.createRule(bulk_rules, policy_id)
elapsed_time = time.time() - start_time
print("Elapsed time: ", elapsed_time, " seconds")



#
# Non Bulk method
#
print(f"Creating {number_of_non_bulk_rules*number_of_ACLs} ACLs with non bulk method")

non_bulk_rules = []

while number_of_non_bulk_rules > 0:
    for num in range(1, number_of_ACLs+1):
        network = "1.1."+str(number_of_non_bulk_rules)+"."+str(num)
        access_rule = {
            "action": "ALLOW",
            "enabled": True,
            "type": "AccessRule",
            "sendEventsToFMC": True,
            "vlanTags": {},
            "sourceNetworks": {
                "literals": [
                  {
                    "type": "Network",
                    "value": network
                  }
                ]
            },
            "logBegin": False,
            "logEnd": True,
            "logFiles": False,
            "name": network + "-to-any"
        }
        non_bulk_rules.append(access_rule)
    number_of_non_bulk_rules = number_of_non_bulk_rules - 1
#
# Non Bulk method
#
def backline():        
    print('\r', end='') 

start_time = time.time()
i=1
for rule in non_bulk_rules:
  print(i, end='')                        # just print and flush
  backline()  
  fmc.createRuleNonBulk(rule, small_policy_id)
  i=i+1

elapsed_time = time.time() - start_time
print("Elapsed time:", elapsed_time, " seconds")

"""
print("Would you like to cleanup? [1/0]")
cleanup = input()
if bool(int(cleanup)) is not False:
    fmc.deletePolicy(small_policy_id)
"""
