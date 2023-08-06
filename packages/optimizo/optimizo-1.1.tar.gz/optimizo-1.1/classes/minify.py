import css_html_js_minify as minify_res

class Minify:
    def __init__(self):
        pass
    
    def html_file(self, file_name, overwrite=False):
        minify_res.process_single_html_file(file_name, overwrite)
    
    def js_file(self, file_name, overwrite=False):
        minify_res.process_single_js_file(file_name, overwrite)
    
    def css_file(self, file_name, overwrite=False):
        minify_res.process_single_css_file(file_name, overwrite)
    
    def html_str(self, string):
        return minify_res.html_minify(string)
    
    def js_str(self, string):
        return minify_res.js_minify(string)
    
    def css_str(self, string):
        return minify_res.css_minify(string,  comments=False)
    
    






