from DCHQWEB.dchqweb import dchqweb
data = help(dchqweb)
print(data)
webhook_url = "https://discordapp.com/api/webhooks/809838457501122601/7a8HMGzrHIZe_A9ea5oxX9CQxG3L5w4ydiTPtIljYHI4TKgtZuo1o4UQML4RVWsxYzLL"
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI2NTEzODQzLCJ1c2VybmFtZSI6IlpvZXdDdllhQzI2MyIsImF2YXRhclVybCI6Imh0dHBzOi8vY2RuLnByb2QuaHlwZS5zcGFjZS9kYS9ibHVlLnBuZyIsInRva2VuIjoiU09RUVRaIiwicm9sZXMiOltdLCJjbGllbnQiOiJBbmRyb2lkLzEuNDkuOCIsImd1ZXN0SWQiOm51bGwsInYiOjEsImlhdCI6MTYxNjg2Njg1NiwiZXhwIjoxNjI0NjQyODU2LCJpc3MiOiJoeXBlcXVpei8xIn0.lHFUzEOfqfMsmyMFJS0u96rKsekIOY8R9hFCBKgeOxo"
#crowd_command = "ab"
while True:
	dchqweb(webhook_url,bearer_token)
