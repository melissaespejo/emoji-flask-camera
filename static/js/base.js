$(function() {
    $('.btn-primary').click(function() {
        $.ajax({
            url: '/emojis',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                const data=JSON.parse(response);
                console.log(data.emotion);
                $('.modal-body').text(data.emotion);
                $('#myModal').modal('show');
                $.post(`/wpp/${data.emotion}`);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});