import time
import asyncio
import boto3
# import os
# from s3util.utils.pathparser import pathparser
# def main(prefix):
#         client = boto3.client('s3')
#         start=time.time()
#         [bucket, directory, incompletepath]= pathparser(prefix)
#         if(os.path.isfile("/tmp/"+bucket+directory[:-1])):
#             file1 = open("/tmp/"+bucket+directory[:-1], 'r')
#             paths=file1.read()
#             print(time.time()-start)
#             return tuple(paths.split("THEDELIMETER"))
#         if(bucket==''):
#             return ()
#         if(directory=='' or directory=='/'):
#             result = client.list_objects(Bucket=bucket, Delimiter='/')
#         else:
#             result = client.list_objects(Bucket=bucket, Prefix=directory, Delimiter='/')
#         allpath=[]
#         if('CommonPrefixes' in result):
#             pref = ['s3://'+bucket+'/'+i['Prefix'] for i in result['CommonPrefixes']]
#             allpath=allpath+pref
#         if 'Contents' in result:
#             cont=['s3://'+bucket+'/'+i['Key'] for i in result['Contents']]
#             allpath=allpath+cont
#         print(time.time()-start)
#         return tuple(allpath)

# print(main("s3://bidgely-artifacts2/rpms/build-custom-"))
loop = asyncio.get_event_loop()

async def filewirte():
    client = boto3.client('s3')
    result =  client.list_objects(Bucket="bidgely-artifacts2", Prefix="rpms/", Delimiter='/')
    file1 = open('myfile.txt', 'w')
    s = "THEDELIMETER".join(result)
    file1.write(s)
    file1.close()
    return 0

async def main(pref):
    start=time.time()
    a = filewirte()
    print(time.time()-start)
    return 0

import time
server = loop.run_until_complete(main("daw"))
