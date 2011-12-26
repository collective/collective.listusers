$(document).ready(function () {
    var clmns = [];

    // filter out vcard column when exporting
    $('#example th').each(function (i, value) {
        if ($(value).text() !== 'vcard') {
            clmns.push(i)
        }
    });

    $("#example").dataTable({
        sDom: 'T<"clear">lfrtip', // where in DOM to inject TableTools controls
        oTableTools: {
            sSwfPath: portal_url + "/++resource++jquery.datatables/extras/TableTools/media/swf/copy_cvs_xls.swf",
            aButtons: [{sExtends: "csv", mColumns: clmns}, {sExtends: "copy", mColumns: clmns}]
        },
        sPaginationType: "full_numbers"
    });
});
