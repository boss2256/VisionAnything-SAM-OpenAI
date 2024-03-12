$(document).ready(function() {
    $('.delete-btn').click(function(e) {
        e.preventDefault();
        var userId = $(this).data('id');  // Assuming you have a data-id attribute for the user's ID
        if (confirm('Are you sure you want to delete this user?')) {
            $.ajax({
                url: '/user/delete/' + userId,
                method: 'POST',
                success: function(response) {
                    // Reload the page or update the user list
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    alert('An error occurred while deleting the user.');
                }
            });
        }
    });
});
