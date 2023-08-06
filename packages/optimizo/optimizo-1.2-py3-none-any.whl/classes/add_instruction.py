import os
import json

class AddInstruction:
    def __init__(self,group, name, target_dir):
        self.group = group
        self.name = name
        self.target_dir = target_dir
        
        self.retry_adding = 0
    
        
        if (self.name == "move"):
            self.get_move()
        elif (self.name == "copy"):
            self.get_copy()
        elif (self.name == "replace"):
            self.get_replace()
        elif (self.name == "minify"):
            self.get_minify()
        elif (self.name == "command"):
            self.get_command()

        
        
    def add_instruction(self, instruction_object):
        filepath = os.path.join(self.target_dir, "optimizo.json")
        with open(filepath) as obj:
            try:
                data = json.load(obj)
                
                if self.group in data.keys():
                    data[self.group].append(instruction_object)
                else:
                    data[self.group] = []
                    data[self.group].append(instruction_object)
                    
                with open(filepath, "w") as outfile:
                    json.dump(data, outfile)
            except json.decoder.JSONDecodeError:
                with open(filepath, "w") as outfile:
                    data = {}
                    
                    with open(filepath, "w") as outfile:
                        json.dump(data, outfile)
                        
                if self.retry_adding < 2:
                    self.add_instruction(instruction_object)
                else:
                    print("[-] Couldnt add instruction, exiting")
                        
        print("[+] Added")
                    
        
        
    def get_move(self):
        print("\nMOVE INSTRUCTION:\n")
        source_file = input("Source File: ")
        dest_file = input("Dest Directory: ")
        
        if (os.path.exists(os.path.abspath(source_file))):
            if os.path.exists(os.path.abspath(dest_file)):
                if (os.path.isdir(os.path.abspath(dest_file))):
                    self.add_instruction(
                        {
                            "name": self.name,
                            "src": os.path.abspath(source_file),
                            "dst": os.path.abspath(dest_file)
                        }
                    )
                else:
                    print("[-] Destination file is not a directory, exiting")
            else:
                print("[-] Destination directory doesnt exist, exiting...")
        else:
            print("[-] Source file doesnt exist, exiting...")
            
    def get_copy(self):
        print("\nCOPY INSTRUCTION:\n")
        source_file = input("Source File: ")
        dest_file = input("Dest Directory: ")
        
        if (os.path.exists(os.path.abspath(source_file))):
            if os.path.exists(os.path.abspath(dest_file)):
                if (os.path.isdir(os.path.abspath(dest_file))):
                    self.add_instruction(
                        {
                            "name": self.name,
                            "src": os.path.abspath(source_file),
                            "dst": os.path.abspath(dest_file)
                        }
                    )
                else:
                    print("[-] Destination file is not a directory, exiting")
            else:
                print("[-] Destination directory doesnt exist, exiting...")
        else:
            print("[-] Source file doesnt exist, exiting...")
        
    def get_replace(self):
        print("\nREPLACE INSTRUCTION:\n")
        source_file = input("Source File: ")
        search_str = input("Search String: ")
        repl_str = input("Replace String: ")
        
        file_name = os.path.abspath(source_file)
        
        if os.path.exists(file_name):
            if (os.path.isfile(file_name)):
                self.add_instruction({
                    "name": self.name,
                    "src": file_name,
                    "search": search_str,
                    "replace": repl_str
                })
            else:
                print("[-] File must be an actual file XD")
        else:
            print("[-] File doesnt exist")
            
    def get_minify(self):
        print("\nMINIFY INSTRUCTION:\n")
        source_file = input("Source File: ")
        
        file_name = os.path.abspath(source_file)
        
        if os.path.exists(file_name):
            if (os.path.isfile(file_name)):
                self.add_instruction({
                    "name": self.name,
                    "src": file_name,
                
                })
            else:
                print("[-] File must be an actual file XD")
        else:
            print("[-] File doesnt exist")
            
    def get_command(self):
        print("\nCOMMAND INSTRUCTION:\n")
        command = input("Command: ")

        self.add_instruction({
                    "name": self.name,
                    "command": command
                
        })
        
        
        
        
    