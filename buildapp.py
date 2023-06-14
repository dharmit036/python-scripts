import subprocess
import os,argparse
import logging
import asyncio

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()
async def install_python_modules(path):
    try:
      os.chdir(os.path.normpath(path))
      if 'requirements.txt' not in os.listdir():
         raise Exception("Missing requirements.txt file")
      subprocess.run(["pip3","install","-r","requirements.txt"],stdout=True)
    except Exception as err:
       logger.error(err)

async def install_npm_modules(path):
   try:
      os.chdir(os.path.normpath(path))
      if "package.json" not in os.listdir():
         raise Exception("Missing package.json file")
      subprocess.run(["npm","install","package.json"], stdout=True)
      return True
   except Exception as err:
      logger.error(err)

async def build_react_project(path,project,envList=[]):
   try:
      os.chdir(os.path.normpath(path))
      port = str(8080)
      if "node_modules" not in os.listdir():
         await install_npm_modules(path)
      if len(envList) > 0:
         subprocess.run(["touch",".env"])
         envFile = open('.env', 'w+')
         for i in range(len(envList)):
            reactEnv = "REACT_APP_"+envList[i]+"\n"   
            envFile.write(reactEnv)
            if envList[i].startswith("PORT"):
               port = str(envFile[i])
         envFile.close()
      subprocess.run(["npm","run","build"], stdout=True)
      logger.info("Build process for react app has been completed")
      if "build" in os.listdir():
         subprocess.run(["pm2","serve", "build/", port, "--spa", "--name", "awesome-react-project"], stdout=True)
      if project == "mern":
         subprocess.run(["pm2","start","app.js","--name","awesome-mern-project"], stdout=True)
   except Exception as err:
      logger.error(err)

async def run_job(path,project,envVars=[]):
    if project.lower() == "python":
       await install_python_modules(path)
    elif project.lower() == "react" or project.lower() == "mern":
       verify_installation = await install_npm_modules(path)
       if verify_installation:
         await build_react_project(path,project,envVars)
       logging.debug("Build completed!")
    else:
       warning_msg = "Sorry, we haven't added a support for "+project+" projects! We'll add support for that very soon :)"
       logging.warning(warning_msg)

async def main():
    try:
      parser = argparse.ArgumentParser()
      parser.add_argument("--env_var",help="Add your custom variables using this flag",action="append",required=False,metavar=("Environment variables used in project"))
      parser.add_argument("--path",help="File path of the project",required=True,metavar=("Project's folder path"))
      parser.add_argument("--project_type",help="Type of the project i.e. Python, React, etc.",required=True,metavar=("Project engine"))
      args = parser.parse_args()
      envVars,path,project=args.env_var,args.path,args.project_type
      await run_job(path,project,envVars)
    except Exception as err:
       logging.error(err)

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(main())
loop.run_until_complete(task)