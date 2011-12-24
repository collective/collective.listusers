$(document).ready(function () {
    $("#example").dataTable({
        sDom: 'T<"clear">lfrtip', // where in DOM to inject TableTools controls
        oTableTools: {
            sSwfPath: portal_url + "/++resource++jquery.datatables/extras/TableTools/media/swf/copy_cvs_xls.swf",
            aButtons: ["copy", "csv"]
        },
        sPaginationType: "full_numbers"
    });
});
