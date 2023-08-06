// Jupyter Notebook Utilities
JPSLUtils = new Object();
JPSLUtils.insert_newline_at_end_of_current_cell = function(text){
    var lastline = Jupyter.notebook.get_selected_cell().code_mirror.doc.
        lineCount();
    Jupyter.notebook.get_selected_cell().code_mirror.doc.setCursor(lastline,0);
    Jupyter.notebook.get_selected_cell().code_mirror.doc.
         replaceSelection("\n" + text );
    }

JPSLUtils.record_input = function (element){
    var nodetype = element.nodeName.toLowerCase();
    var tempval = ''+element.value;//force to string
    var tempsize = ''+element.size;
    if (tempsize==null){tempsize='7'};
    var tempclass = element.className;
    if (tempclass==null){tempclass=''};
    var tempid = element.id;
    if (tempid==null){tempid=''};
    var tempelem = document.createElement(nodetype);
    tempelem.className =tempclass;
    tempelem.id=tempid;
    tempelem.setAttribute('size',tempsize);
    if (nodetype=='input'){
        tempelem.setAttribute('value',tempval);
    } else {
        tempelem.innerHTML = element.value;
    }
    tempelem.setAttribute('onblur','JPSLUtils.record_input(this)');
    element.replaceWith(tempelem);
}

JPSLUtils.executePython = function(python) {
    return new Promise((resolve, reject) => {
        var callbacks = {
            iopub: {
                output: (data) => resolve(data.content.text.trim())
            }
        };
        Jupyter.notebook.kernel.execute(`print(${python})`, callbacks);
    });
}

JPSLUtils.executePython2 = function(python) {
    return new Promise((resolve, reject) => {
        var callbacks = {
            iopub: {
                output: (data) => resolve(JSON.stringify(data, null, 4))
            }
        };
        Jupyter.notebook.kernel.execute(`print(${python})`, callbacks);
    });
}
JPSLUtils.record_names = function(){
    var currentcell = Jupyter.notebook.get_selected_cell();
    var dlg = document.createElement('div');
    dlg.setAttribute('id','get_names_dlg')
    var tmp = document.createElement('H4');
    var inststr = "In the box below type your name and your partners' names";
    inststr += " (one per line):";
    tmp.innerHTML=inststr
    dlg.append(tmp);
    tmp = document.createElement('div');
    tmp.innerHTML = '<textarea cols="30" onblur="JPSLUtils.record_input(this)"/>';
    dlg.append(tmp);
    $(dlg).dialog({modal:true,
                  close: function(){$(this).dialog('destroy')},
                  buttons:[
                  {text: 'Cancel',
                  click: function(){$(this).dialog('destroy')}},
                  {text: 'OK/Do It',
                  click: function(){var rcrd = document.getElementById(
                                    'Last-User');
                                    var parent = rcrd.parentNode;
                                    var dlg = document.getElementById(
                                    'get_names_dlg');
                                    var textboxes = dlg.querySelectorAll(
                                    "textarea");
                                    var tmp = document.createElement('div');
                                    tmp.setAttribute('id','Grp-names');
                                    tmp.
                                    setAttribute('style','font-weight:bold;');
                                    var refeed = /\r?\n|\n\r?|\n/g;
                                    var tmpstr = 'Partners: '+ textboxes[0]
                                    .innerHTML.replace(refeed,'; ');
                                    //tmpstr.replace(refeed,'; ');
                                    tmp.innerHTML = tmpstr;
                                    tmpstr = '# '+rcrd.innerHTML +'\n# '
                                    +tmpstr;
                                    //rcrd.append(tmp);
                                    JPSLUtils.
                                    insert_newline_at_end_of_current_cell(
                                    tmpstr);
                                   $(this).dialog('destroy');}}
                  ]})
    Jupyter.notebook.focus_cell();//Make sure keyboard manager doesn't grab inputs.
    Jupyter.notebook.keyboard_manager.enabled=false;
    dlg.focus();
    Jupyter.notebook.keyboard_manager.enabled=false; //Make sure keyboard manager doesn't grab inputs.
}