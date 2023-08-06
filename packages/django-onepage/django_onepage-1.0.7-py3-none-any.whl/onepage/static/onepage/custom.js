$(document).ready(function() {
    //set initial state.
    $('#activityStatus').val(this.checked);

    $('#activityStatus').change(function() {
        let status = this.checked;
        if(status) {
            var returnVal = confirm("Are you sure to open the restaurant?");
            $(this).prop("checked", returnVal);
            if (returnVal){
                console.log('api request for update......');
                $.ajax({
                    url: '/ajax/update-restaurants/',
                    data: {
                        'status': 'Open'
                    },
                    dataType: 'json',
                    success: function (data) {
                        console.log(data);
                        $('#restaurant_status').html('Restuarant Open');
                        $('#restaurant_status').removeClass('btn-Closed');
                        $('#restaurant_status').addClass('btn-Open');
                        Swal.fire({
                              position: 'top-end',
                              icon: 'success',
                              title: 'Restaurant Status Updated Successfully',
                              showConfirmButton: false,
                              timer: 1500
                            })
                    }
                  });
            }
        }
        if(!status){
            var returnVal = confirm("Are you sure to close the restaurant?");
             $(this).prop("checked", !returnVal);
             if (returnVal){
                console.log('api request for update .......');

                $.ajax({
                    url: '/ajax/update-restaurants/',
                    data: {
                        'status': 'Closed'
                    },
                    dataType: 'json',
                    success: function (data) {
                        console.log(data);
                        $('#restaurant_status').html('Restuarant Closed');
                         $('#restaurant_status').removeClass('btn-Open');
                        $('#restaurant_status').addClass('btn-Closed');
                        Swal.fire({
                              position: 'top-end',
                              icon: 'success',
                              title: 'Restaurant Status Updated Successfully',
                              showConfirmButton: false,
                              timer: 1000
                            })
                    }
                  });
             }
        }
    });

    function customAjaxSubmitFunction(e) {
        e.preventDefault();

        var form_id = e['target'].id
        var form = $("#" + form_id);
        var method = form.attr('method');
        var data_url = form.attr('data-url');
        var data_modal_id = form.attr('data-modal-id');

        var modal = $("#" + data_modal_id);

        modal.removeClass('md-show')
        modal.modal('hide')

        $.ajax({
            url: form.attr('data-url'),
            method: form.attr('method'),
            data: new FormData(form.get(0)),
            cache: false,
            processData: false,
            contentType: false,

            success: function(data){
                location.reload()
            },

            error: function(data){
                var modal = $("#" + data_modal_id);

                console.log(data)

                swal("Query not proceed", data.responseJSON.error, "error");

                modal.addClass('md-show')
                modal.modal('show')
            }
        })
    }

    var form_list = document.getElementsByTagName("form");

    for (var i = 0; i < form_list.length; i++) {
        var form_id = form_list[i].id;

        if (form_id.startsWith('ajax')){
            var form = $("#" + form_id);

            form.on('submit', function(e){
                console.log('called form', e)
                customAjaxSubmitFunction(e, form_id)
            })
        }
    }

    $('.table-entry-edit').on('click', function() {
      let tr = $(this).closest('tr');
      let td = tr.find('td');

      let result = {
        'data_modal_id': 'exampleDemoEditModal',
        'form_id': $(this).attr('data-form-id'),
        'id': tr.attr('data-id')
      };

      for (var i = 0; i < td.length; i++) {
        result[td.get(i).className] = td.get(i).innerText
      }

      $.ajax({
        url: $(this).attr('data-url'),
        method: $(this).attr('data-method'),
        data: result,

        success: function(data){
            console.log('success', data)
            var change_div_holder = $('#exampleDemoEditModal');
            var change_div = $('#editModalFormHolder');

            change_div.html(data['html']);
            change_div_holder.modal('show');

            var form_id = data['requestBody']['form_id']
            var form = $("#" + form_id);

            form.on('submit', function(e){
                customAjaxSubmitFunction(e)
            })
        },

        error: function(data){
            console.log('error', data)
        }
      })
    });

    $('.table-entry-delete').on('click', function() {
        var tr = $(this).closest('tr');
        var td = tr.find('td');

        var url = $(this).attr('data-url');
        var method = $(this).attr('data-method');

        swal({
          title: "Are you sure?",
          text: "You will not be able to recover this item!",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "Yes, delete it!",
          closeOnConfirm: false
        },
        function(isConfirm){
          if (isConfirm) {
            $.ajax({
                url: url,
                method: method,
                data: {
                    id: tr.attr('data-id')
                },
                success: function(data){
                    swal("Deleted!", "Request item is permanently deleted.", "success");
                    location.reload();
                },
                error: function(data){
                    swal("Error", "Check file exist and you have right permission.", "error");
                    location.reload();
                }
            })
          } else {
            swal("Canceled!", "Delete request canceled by the User.")
          }
        });

    })

    $('.ajax-four-act-handler').on('click', function() {
        console.log($(this))
        ajaxFourActHandler($(this))
    });

});
