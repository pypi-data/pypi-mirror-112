
class FilesOperater():
    def read(file:str, seperator=None, type="str"):
        type=type.lower()
        if type=="list":
            try:
                f = open(file,"r")
                rd = f.read()
                f.close()
                return rd.split(seperator)
            except Exception as e:
                return f"Exception Occured: {e}"
        elif type=="str":
            try:
                f = open(file,"r")
                rd = f.read()
                f.close()
                return rd
            except Exception as e:
                return f"Exception Occured: {e}"
        else:return "Incorect Argument. type=str (For Result in normal Strings); type=list (For results in list form); Default is str"

    
    def write(file:str, content):
        try:
            f = open(file,"w")
            f.write(f"{content}\n")
            f.close()
            return f"File \"{file}\" has been formatted successfully."
        except Exception as e:
            return f"Exception Occured: {e}"

    def edit(file:str, content):
        try:
            f = open(file,"a")
            f.write(f"{content}\n")
            f.close()
            return f"File \"{file}\" has been Edited Successfully."
        except Exception as e:
            return f"Exception Occured: {e}"
