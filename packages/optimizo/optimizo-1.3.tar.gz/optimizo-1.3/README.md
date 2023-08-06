# Optimizo
Optimizo its an tool that allows to set up instructions and run them later. In the mean you will have to run them manually using 

`python optimizo.py -r group_name`


## How to Install: For users
1. Clone it 

`pip install optimizo`

2. Play

`python -m optimizo -h`

## How to Install: For developers
1. Clone it 

`git clone https://github.com/takumade/Optimizo.git`

2. Install Requirements

`cd Optimizo && pip install -r requirements`

3. Play

`python optimizo.py -h`


## For Contributors

1. Class name are in camel case e.g `KillServer`
2. Variables, Functions and Methods should be in snake case e.g `kill_server`
3. File names should be in snake_case e.g `push_to_github.py`
4. Instructions are executed from `classes/run_instructions.py`
5. Instructions are added from `classes/add_instructions.py`


## How does it work

1. You create your config file
      `optimizo.py -c`   OR  `optimizo.py -c -w .`

    It will generate something like this:
    
```
{
    "develop": [{
        "name": "copy",
        "src": "C:\\xampp\\htdocs\\projects\\Optimizo\\config.py",
        "dst": "C:\\xampp\\htdocs\\projects\\Optimizo\\classes"
    }, {
        "name": "replace",
        "src": "C:\\xampp\\htdocs\\projects\\Optimizo\\config.py",
        "search": "excluded_folders",
        "replace": "excluded_beans"
}]}
```

2. You then add your instructions like this

    #### Method 1: Interactive
     `optimizo.py -g develop -a`


    #### Method 2: Semi-Interactive
    `optimizo.py -g develop -i move`



     It will ask you for instruction name and extra details.
     You can also add multiple instructions like these

     **Note:** Develop here is a group name in your config, it can be `cats, chickens, deploy, hide, etc`

     **Note:*** If a group is not available it is added

3. Run your group of instruction
    `optimizo.py -r develop`
    
**Note:** If you know what you are doing you can manually modify `optimizo.json`
**Note:** Instructions are run one after the other.

## Instructions

Here is a list of supported intructions


| Instruction | Description | Implemented|
| ----------- | ----------- |------------|
| move | Move a file from one part to another | Yes
| copy | Copy a file from source to dest | Yes
| replace | Replace text in a file | Yes
| minify | Minify text in a file | Yes
| command | Execute a command | Yes


### What am i doing with this tool
- I use it optimize and deploy my Laravel and Python projects
- I use to automate some menial tasks
