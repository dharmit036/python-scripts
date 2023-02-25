import os,subprocess
import argparse
import logging
import asyncio

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()

async def install_python_modules(path):
    try:
        os.chdir(os.path.normpath(path))
        if 'requirements.txt' not in os.listdir():
            raise Exception("Missing requirements.txt file")
        else:
            subprocess.run(["pip3","install","-r","requirements.txt"], stdout=True)
    except Exception as err:
        logging.error(err)

async def install_npm_modules(path):
    try:
        os.chdir(os.path.normpath(path))
        if "package.json" not in os.listdir():
            raise Exception("Missing package.json file")
        subprocess.run(["npm","install","package.json"],stdout=True)
        return True
    except Exception as err:
        logging.error(err)

async def build_react_project(path,project,envList=[]):
    try:
        os.chdir(os.path.normpath(path))
        process_port = str(8080)
        if "node_modules" not in os.listdir():
            await install_npm_modules(path)
        if len(envList)>0:
            subprocess.run(["touch",".env"])
            envFile = open('.env','w+')
            for i in range(len(envList)):
                if project.lower() == "react":
                    reactEnv = "REACT_APP_"+envList[i]+"\n"
                    envFile.write(reactEnv)
                else:
                    env = envList[i]+"\n"
                    envFile.write(env)
                if envList[i].startswith("PORT"):
                    temp = envList[i].split("=")
                    port = str(temp(len(temp)-1))
                    process_port = port
            envFile.close()
        if project.lower() == "react":
            subprocess.run(["npm","run","build"],stdout=True)
            subprocess.run(["pm2","serve","build/",process_port,"--spa","--name","awesome-react-project"],stdout=True)
        if project.lower() == "mern" and "app.js" is os.listdir():
            subprocess.run(["pm2","start","app.js","--name","awesome-mern-project"],stdout=True)  
    except Exception as err:
        logger.error(err)

async def run_job(path, project, envVars=[]):
    try:
        if project.lower() == "python":
            await install_python_modules(path)
        elif project.lower() == "react" or project.lower() == "mern":
            verify_installation = await install_npm_modules(path)
            if verify_installation:
                await build_react_project(path,project,envVars)
            logging.debug("Build completed!")
    except Exception as err:
        logger.error(err)

async def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--env_var",help="Add your custom environment variables",action="append",required=False,metavar=("Environment variables used in project"))
        parser.add_argument("--path",help="Path to the project",required=True,metavar=("Project's folder path"))
        parser.add_argument("--project_type",help="Type of the project. i.e. Python, MERN, etc.", required=True,metavar=("Project language"))
        args = parser.parse_args()
        envVars,path,project=args.env_var,args.path,args.project_type
        await run_job(path, project, envVars)
    except Exception as err:
        logging.error(err)