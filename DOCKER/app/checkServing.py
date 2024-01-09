import os
import datetime
import gc

cmd = "cd /app/app/ && python3 create_serve_models.py"

def main():
    try:
        t_wait = int(os.getenv('DAEMONSECS', default=10))
    except:
        t_wait = 10
        
    reseted = False
    
    while True:
        
        d = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        if (datetime.datetime.now()-d).seconds < 300 and reseted == False: # reset int the first 5 minutes of the day.
            gc.collect()
            os.system(cmd)
            reseted = True
        elif (datetime.datetime.now()-d).seconds < 300 and reseted == True:
            pass
        else:
            reseted = False

        if os.path.exists('/app/app/gunicorn.sock') ==  False:
            gc.collect()
            os.system(cmd)
            
        time.sleep(t_wait)

if __name__ == "__main__":
    main()
