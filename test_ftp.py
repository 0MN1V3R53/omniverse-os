import ftplib

try:
    ftp = ftplib.FTP()
    ftp.connect('82.198.228.154', 21, timeout=10)
    ftp.login('u803913036', 'cunt3344#')
    print("FTP login successful!")
    ftp.cwd('domains/skyautoservices.com/logs')
    print(ftp.nlst())
    ftp.quit()
except Exception as e:
    print(f"FTP Error: {e}")
