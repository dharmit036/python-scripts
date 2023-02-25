# python-scripts
Random python scripts I've created for DevOps tasks

## Script for building and launching Python or MERN projects
- `app_builder.py` is used to launch/automate the steps of create builds for Python or MERN projects
- The focus of this script includes preparation of environment for relative programming language and to install listed dependencies
- User can also define their custom environment variables, which will be used in project. Here's the sample command to play with script:

```shell
  python app_builder.py --path '/Path/to/project' --project_type 'mern' \
                        --env_var ENV1=KEY1 \
                        --env_var ENV2=KEY2
```