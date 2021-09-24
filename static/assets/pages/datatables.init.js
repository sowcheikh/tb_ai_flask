/*
 Template Name: Zoter - Bootstrap 4 Admin Dashboard
 Author: Mannatthemes
 Website: www.mannatthemes.com
 File: Datatable js
 */

$(document).ready(function() {
    $('#datatable').DataTable();
    /*****************************************TABLEAU BORD AI & CR ****************************/

    //Tableau de bord AI
    var table_tb_ai = $('#datatable-buttons-tb-ai').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "order": [0, 'desc'],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [0, 2, 3, 5, 6, 9, 11, 12, 13, 14, 16], className: 'hidden' }
        ]
    });
    table_tb_ai.buttons().container()
        .appendTo('#datatable-buttons-tb-ai_wrapper .col-md-6:eq(0)');

    //Tableau de bord CR AI
    var table_tb_cr_ai = $('#datatable-buttons-tb-cr-ai').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                    doc.styles.tableHeader.alignment = 'left';
                    doc.content.forEach(function(item) {
                        if (item.table) {
                         item.table.widths = ["*", 550] 
                        } 
                    });
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "order": [0, 'desc'],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [2],className: 'hidden' }
        ]
    });
    table_tb_cr_ai.buttons().container()
        .appendTo('#datatable-buttons-tb-cr-ai_wrapper .col-md-6:eq(0)');
    
    //Tableau de bord CR
    var table_tb_cr = $('#datatable-buttons-tb-cr').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                            return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                            return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                            return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "order": [0, 'desc'],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15],className: 'hidden' }
        ]
    });
    table_tb_cr.buttons().container()
        .appendTo('#datatable-buttons-tb-cr_wrapper .col-md-6:eq(0)');
    
    //Tableau de bord CR ALL
    var table_tb_cr_all = $('#datatable-buttons-tb-cr-all').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                
                title: function () { return $('.header-title').html(); },
                orientation: 'landscape',
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                    doc.styles.tableHeader.alignment = 'left';
                    doc.content.forEach(function(item) {
                        if (item.table) {
                         item.table.widths = ["*", "*", 450] 
                        } 
                    });
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "order": [0, 'desc'],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [3],className: 'hidden' }
        ]
    });
    table_tb_cr_all.buttons().container()
        .appendTo('#datatable-buttons-tb-cr-all_wrapper .col-md-6:eq(0)');
    
    /*****************************************RAPPORTS AI ****************************/

    //Tableau de bord CR
    var table_rapport_ai = $('#datatable-buttons-rapport-ai').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "ordering": false,
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [0],className: 'hidden' }
        ]
    });
    table_rapport_ai.buttons().container()
        .appendTo('#datatable-buttons-rapport-ai_wrapper .col-md-6:eq(0)');
    /*****************************************PERSONNEL AI ****************************/
    //Tableau de bord CR
    var table_agent = $('#datatable-buttons-agent').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [4,8],className: 'hidden' }
        ]
    });
    table_agent.buttons().container()
        .appendTo('#datatable-buttons-agent_wrapper .col-md-6:eq(0)');
    /******************************** CARTOGRAPHIE DES COMPETENCES **************************/

    var table_carto = $('#datatable-buttons-carto').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "columnDefs": [   
            { targets: [0, 1], visible: true},   
            { targets: '_all', visible: false }
        ],
        'rowsGroup': [0]
    });
    table_carto.buttons().container()
        .appendTo('#datatable-buttons-carto_wrapper .col-md-6:eq(0)');

        
    /*****************************************TABLEAU SUIVI CR ****************************/

    //Buttons examples
    var table_cr = $('#datatable-buttons-cr').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "ordering": false,
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [4, 5, 10, 11],className: 'hidden' }
          ]
    });
    table_cr.buttons().container()
        .appendTo('#datatable-buttons-cr_wrapper .col-md-6:eq(0)');
    
    /*****************************************TABLEAU STRUCTURE ****************************/
    var table_structure = $('#datatable-buttons-structure').DataTable({});
    table_structure.buttons().container()
        .appendTo('#datatable-buttons-structure_wrapper .col-md-6:eq(0)');
        
    /*****************************************TABLEAU FILIALES ****************************/

    //Tableau OSL
    var table_osl = $('#datatable-buttons-osl').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: ['copy', 'excel', 'pdf'],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_osl.buttons().container()
        .appendTo('#datatable-buttons-osl_wrapper .col-md-6:eq(0)');
    
    //Tableau OGC
    var table_ogc = $('#datatable-buttons-ogc').DataTable({
        scrollX: true,
        scrollCollapse: true,
        buttons: ['copy', 'excel', 'pdf'],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_ogc.buttons().container()
        .appendTo('#datatable-buttons-ogc_wrapper .col-md-6:eq(0)');
    
    //Tableau OGB
    var table_ogb = $('#datatable-buttons-ogb').DataTable({
        lengthChange: false,
        buttons: ['copy', 'excel', 'pdf'],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_ogb.buttons().container()
        .appendTo('#datatable-buttons-ogb_wrapper .col-md-6:eq(0)');

    //Tableau OML
    var table_oml = $('#datatable-buttons-oml').DataTable({
        lengthChange: false,
        buttons: ['copy', 'excel', 'pdf'],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_oml.buttons().container()
        .appendTo('#datatable-buttons-oml_wrapper .col-md-6:eq(0)');
    
    /*****************************************TABLEAU SUIVI REPORT ****************************/

    //Tableau Suivi Report
    var table_report = $('#datatable-buttons-report').DataTable({
        lengthChange: false,
        buttons: ['copy', 'excel', 'pdf'],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_report.buttons().container()
        .appendTo('#datatable-buttons-report_wrapper .col-md-6:eq(0)');

    /*****************************************TABLEAU REPORTING CODIR *************************/

    //Reporting Codir AI
    var table_codir_ai = $('#datatable-buttons-codir-ai').DataTable({
        lengthChange: false,
        scrollX: true,
        scrollCollapse: true,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                      body: function ( data, column, row ) {
                        return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                      }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                    doc.styles.tableHeader.alignment = 'left';
                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [],className: 'hidden' }
        ],
        "ordering": false,
        "paging": false,
        "info": false,
        "searching": false
    });
    table_codir_ai.buttons().container()
        .appendTo('#datatable-buttons-codir-ai_wrapper .col-md-6:eq(0)');

    //Reporting Codir CR
    var table_codir_cr = $('#datatable-buttons-codir-cr').DataTable({
        lengthChange: false,
        buttons: [{
                extend: 'copy',
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'excel',
                title: function () { return $('.header-title').html(); },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)'
                }
            },
            {
                extend: 'pdf',
                orientation: 'landscape',
                title: function () { return $('.header-title').html(); },
                customize: function(doc) {
                    doc.styles.tableHeader.fillColor = '#ee7627';
                    doc.styles.tableHeader.alignment = 'left';

                },
                exportOptions: {
                    stripHtml: false,
                    format: {
                        body: function ( data, column, row ) {
                          return (column === 0) ? data.replace( /\n/g, '"&CHAR(10)&CHAR(13)&"' ) : data.replace(/(&nbsp;|<([^>]+)>)/ig, "");
                        }
                    },
                    columns: ':visible:not(.action)' 
                }
            },
            'colvis'
        ],
        "columnDefs": [
            // Hide second, third and fourth columns
            { "visible": false, "targets": [],className: 'hidden' }
        ],
        "ordering": false,
        "info": false,
    });
    table_codir_cr.buttons().container()
        .appendTo('#datatable-buttons-codir-cr_wrapper .col-md-6:eq(0)');
} );
