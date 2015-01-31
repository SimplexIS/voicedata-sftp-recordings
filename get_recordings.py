#!/usr/bin/env python
import paramiko
import os
import tarfile

def main():
    basepath = '.'
    pkey = paramiko.RSAKey.from_private_key_file('~/.ssh/id_rsa')
    transport = paramiko.Transport(('89.184.172.214', 22))
    transport.connect(username='*USER_NAME*', pkey=pkey)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir('data')
    sftp.chdir('monitor')

    for year in sftp.listdir('.'):
        sftp.chdir(year);
        for month in sftp.listdir('.'):
            sftp.chdir(month)
            for day in sftp.listdir('.'):
                sftp.chdir(day)
                for file in sftp.listdir('.'):
                    if not os.path.exists(get_directory(year, month, day)):
                        os.makedirs(get_directory(year, month, day))

                    sftp.get(file, get_filepath(year, month, day, file))
                    sftp.remove(file)
                    tar = tarfile.open(get_filepath(year, month, day, file))
                    tar.extractall(get_directory(year, month, day))
                    tar.close()
                    os.remove(get_filepath(year, month, day, file))

                    if os.path.isfile(get_csvpath(year, month, day)):
                        with open(get_csvpath(year, month, day), 'a') as outfile:
                            with open(get_csvtarpath(year, month, day, file)) as infile:
                                next(infile)
                                for line in infile:
                                    outfile.write(line)
                        os.remove(get_csvtarpath(year, month, day, file))
                    else:
                        os.rename(get_csvtarpath(year, month, day, file), get_csvpath(year, month, day))
                sftp.chdir('..')
            sftp.chdir('..')
        sftp.chdir('..')
    sftp.close()

def get_directory(year, month, day):                                            
    return basepath + '/' + year + '/' + month + '/' + day                  
                                                                                        
def get_filepath(year, month, day, file):                                       
    return get_directory(year, month, day) + '/' + file
                                                                                                
def get_csvtarpath(year, month, day, file):
    return get_filepath(year, month, day, file)[:-3] + 'csv'

def get_csvpath(year, month, day):
    return get_directory(year, month, day) + '/' + day + '-' + month + '-' + year + '.csv'

if __name__ == "__main__":
    main()
