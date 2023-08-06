
import os, sys
from classes.add_instruction import AddInstruction
from classes.run_instructions import RunInstructions

class Bootstrap:
    def __init__(self):
        self.interactive_retry = 0
        
        self.instructions = {
            "1": "move",
            "2": "copy",
            "3": "replace",
            "4": "minify",
            "5": "command"
        }
        
        
    def list_instructions(self):
        ins_keys = self.instructions.keys()
        
        for key in ins_keys:
            print("{0}. {1}".format(key , self.instructions[key]))
        
    def get_directory(self, directory):
        if (directory == None):
            target_dir = os.getcwd()
        else:
            target_dir = os.path.abspath(directory)
        
        return target_dir
    
    
    def generate(self, directory):
        print("[*] Generating config file")
        
        target_dir = self.get_directory(directory)
            
        with open(os.path.join(target_dir, "optimizo.json"), "w") as wobj:
            wobj.write("""{}""")
        
        print("[100%] Done")
        
        
    def add_instruction_semi_interactive(self, group, instruction, directory):
        target_dir = self.get_directory(directory)
        add_instruction = AddInstruction(group, instruction, target_dir)
        
    def add_instruction_interactive(self, group, directory):
        
        target_dir = self.get_directory(directory)
        
        
        self.list_instructions()
        
        ins = input("Choose instruction[1-5]: ")
        
  
        try:
            ins = int(ins)
            choosen_ins = instructions[str(ins)]
            add_instruction = AddInstruction(group, choosen_ins, target_dir)
            
             
        except ValueError:
            
            if (self.interactive_retry < 2):
                self.interactive_retry += 1
                print("[-] Please a number between 1-5")
                self.add_instruction_interactive() 
            else:
                print("[-] You dont know what you are doing! Exiting...")
                sys.exit()
        
    def run_instruction(self, group, directory):
       target_dir = self.get_directory(directory) 
       run_inst = RunInstructions(group, target_dir)
        