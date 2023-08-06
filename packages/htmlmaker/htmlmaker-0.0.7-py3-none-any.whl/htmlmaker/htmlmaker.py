import html

def self_test():
    #初始化css
    fp = open('pure-min.css', 'r', encoding='utf-8')
    css = fp.read()
    test_table1 = {"title":"my_good_table1", "headers": ["x","y","z"], "body": [{"x": "Title x", "y": "Title y", "z": "Title z"}, {"x": 1, "y": make_anchor("https://www.google.com", "google", True), "z": 3},{"x": 2, "y": 3, "z": 4}]}
    test_table2 = {"title":"my_good_table2", "headers": ["x","y","z"], "body": [{"x": "Title x", "y": "Title y", "z": "Title z"}, {"x": 1, "y": make_anchor("https://www.google.com", "google", True), "z": 3},{"x": 2, "y": 3, "z": 4}]}

    data = {"tables": [test_table1, test_table2]}
    make_output_html('test.html', data, css)

def make_anchor(url, content, _blank = True):
    '''
    输出 anchor

    '''
    addtional_bl = ""
    if(_blank):
        addtional_bl = ' target="_blank"'
    return "".join(['<a href="', html.escape(url), '"', addtional_bl, '>',content, '</a>'])

def make_output_html(output_path, data, css = ""):
    '''
    以表格形式输出用于流水线展示的报告

    tables 格式为一个 json ，结构如下：

    data 下三个集合：
        title(str): 标题
        headers(list): 有序的表头,对应了row中的key
        body(list): 数据表本体，里面每个数据为一个dict，key需要从 headers 里面找

    {"tables": [{"title":"my_good_table", "headers": ["x","y","z"], "body": [{"x": 1, "y": 2, "z": 3},{"x": 2, "y": 3, "z": 4}]}]}
    '''
    wfp = open(output_path, 'w+', encoding='utf-8')
    
    #生成html头部
    wfp.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>\n")
    wfp.write("\n".join(["<style>", css, "</style>"]))

    row_count = 0
    for table in data["tables"]:
        #生成头部
        wfp.write("\n".join(["<h3>", html.escape(table["title"], quote=True), "</h3>"]))
        wfp.write("<table class=\"pure-table\">")

        row_count = 0
        for row in table["body"]:
            row_data = []
            for col in table["headers"]:
                row_data.append(str(row.get(col, "")))

            if(row_count == 0):
                wfp.write('<thead>')
            elif(row_count == 1):
                wfp.write('<tbody>')
       
            wfp.write("<tr><td>")
            wfp.write('</td><td>'.join(row_data))
            wfp.write("</tr></td>\n")

            if(row_count == 0):
                wfp.write('</thead>')
            row_count = row_count + 1

        wfp.write("</tbody></table>\n")

    wfp.write("</body></html>")

if __name__ == '__main__':
    self_test()