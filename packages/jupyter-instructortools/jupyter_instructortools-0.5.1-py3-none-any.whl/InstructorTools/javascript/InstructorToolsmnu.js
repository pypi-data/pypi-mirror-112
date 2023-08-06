function createInstructorToolsMenu(){
    var donotinstall = Jupyter.notebook.metadata.noinstructortool;
    if (donotinstall){
        alert('Instructor Tools may not be installed in this notebook!');
        deleteInstructorToolsMenuPerm();
        return;
    }
    if(!document.getElementById('InstructorToolsmnu')){
        var newselect=document.createElement('select');
        newselect.id = 'InstructorToolsmnu';
        newselect.classList.add('form-control'); //class to match notebook formatting
        newselect.classList.add('select-xs'); //class to match notebook formatting
        newselect.onchange=function(){
            var lastvalue = this.value;
            this.value='Instructor Tools';
            if (lastvalue=='Insert Data Entry Table...'){
                get_table_dim();
            }
            if (lastvalue=='Protect Selected Cells'){
                protect_selected_cells();
            }
            if (lastvalue=='Deprotect Selected Cells'){
                deprotect_selected_cells();
            }
            if (lastvalue=='Indicate Protected Cells'){
                mark_protected_cells();
            }
            if (lastvalue=='Insert get names and timestamp'){
                insert_getnames_timestamp();
            }
            if (lastvalue=='Deactivate this menu'){
                deleteInstructorToolsMenu();
            }
            if (lastvalue=='!deactivate permanently!'){
                deleteInstructorToolsMenuPerm();
            }
            if (lastvalue=='Insert initialization boilerplate'){
                insert_init_boilerplate();
            }
        }
        var optiontxt = '<option title="Insert an Instructor Tool">Instructor Tools</option>';
        optiontxt+='<option title="Insert cell below selected and create a data entry table.">Insert Data Entry Table...</option>';
        optiontxt+='<option title="Prevent editting of selected cells.">Protect Selected Cells</option>';
        optiontxt+='<option title="Allow editting of selected cells.">Deprotect Selected Cells</option>';
        optiontxt+='<option title="Temporarily highlight protected cells in pink.">Indicate Protected Cells</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Insert get names and timestamp function into current cell. Also locks the cell to editing.">';
        optiontxt+='Insert get names and timestamp</option>';
        optiontxt+='<option title="Insert boilerplate about initialization in next cell">Insert initialization boilerplate</option>';
        optiontxt+='<option title="Remove/deactivate this menu. Use python command `import InstructorTools` to reactivate">';
        optiontxt+='Deactivate this menu</option>';
        optiontxt+='<option title="Remove menu permanently. Blocks reinstalling.">';
        optiontxt+='!deactivate permanently!</option>';
        newselect.innerHTML=optiontxt;
        document.getElementById('maintoolbar-container').appendChild(newselect);
    }
}

function deleteInstructorToolsMenu(){
    if(document.getElementById('InstructorToolsmnu')){
        document.getElementById('InstructorToolsmnu').remove();
    }
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        var should_delete = false;
        if(celllist[i].get_text().indexOf('from InstructorTools import *') !== -1){
            should_delete = true
        }
        if (celllist[i].get_text().indexOf('import InstructorTools')!== -1){
            should_delete = true
        }
        if(celllist[i].get_text().indexOf('instmenu_act()') !== -1){
            should_delete = true
        }
        if (should_delete){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
    }
}
function deleteInstructorToolsMenuPerm(){
    if(document.getElementById('InstructorToolsmnu')){
        document.getElementById('InstructorToolsmnu').remove();
    }
    Jupyter.notebook.metadata.noinstructortool=true;
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if(celllist[i].get_text().indexOf('from InstructorTools import *') !== -1){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
        if(celllist[i].get_text().indexOf('instmenu_act()') !== -1){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
    }
}

function protect_selected_cells(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        celllist[i].metadata.editable=false;
        celllist[i].element.children()[0].setAttribute("style","background-color:pink;");
        }
}

function deprotect_selected_cells(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        celllist[i].metadata.editable=true;
        celllist[i].element.children()[0].removeAttribute("style");
    }
}

function mark_protected_cells(){
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if (celllist[i].metadata.editable==false){
        celllist[i].element.children()[0].setAttribute("style","background-color:pink;");
        } else {
        celllist[i].element.children()[0].removeAttribute("style");
        }
    }
}

function insert_getnames_timestamp(){
    var text = 'import JPSLUtils\nJPSLUtils.record_names_timestamp()';
    JPSLUtils.insert_newline_at_end_of_current_cell(text);
    protect_selected_cells();
}

function insert_init_boilerplate(){
    var mkdstr = "### You must initialize the software each time you use \
    this notebook.\n";
    mkdstr += " 1. First, check that the notebook is \"Trusted\" by looking \
    near";
    mkdstr += " the right of the Jupyter toolbars. If the notebook is not \
    trusted";
    mkdstr += " you need to click on the \"not trusted\" button and trust the";
    mkdstr += " notebook. **You should only trust notebooks that come from a";
    mkdstr += " *trusted source*, such as the class website.**\n";
    mkdstr += " 2. The cell immediately below contains code that loads the";
    mkdstr += " software modules necessary for this notebook to run. It also";
    mkdstr += " collects some bookkeeping information that can be used for";
    mkdstr += " troubleshooting. **You must run this cell each time you use";
    mkdstr += " the notebook or later cells may not work.**\n";
    mkdstr += " 3. If you are doing calculations that depend upon";
    mkdstr += " using variables passed from calculations done the previous";
    mkdstr += " time the notebook was opened, you will need to run those";
    mkdstr += " previous cells to redefine the variables.\n";
    mkdstr += " 4. *DO NOT run cells that contain plot displays of live data";
    mkdstr += " collection, as that will restart the data collection.* You can";
    mkdstr += " reload data collected from the `.csv` files  written for each";
    mkdstr += " collection run. Ideally you would do this in a new notebook.";

  Jupyter.notebook.focus_cell();
  var currentcell = Jupyter.notebook.insert_cell_below();
  currentcell.set_text(mkdstr);
  var cellindex=Jupyter.notebook.find_cell_index(currentcell);
  Jupyter.notebook.to_markdown(cellindex);
  Jupyter.notebook.focus_cell();
  Jupyter.notebook.get_selected_cell().execute();
}