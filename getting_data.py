from sodapy import Socrata
import pandas as pd

client = Socrata('healthdata.gov',
                 '2jXpTjENExA3C29gsCcJcZOxg',
                 username='fco.cervantesrdz@gmail.com',
                 password='FcoRdz.315264978')
results = client.get("g62h-syeh", limit=50000)
table = pd.DataFrame.from_records(results)

table.to_csv('my_table.csv', index=False)