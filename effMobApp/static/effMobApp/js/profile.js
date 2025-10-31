document.addEventListener('DOMContentLoaded', function() {

  bindButton('logout-button', 'logout/');
  bindButton('admin-button', 'adminPage/');
  bindButton('operator-button', 'operatorPage/');
  bindButton('user-button', 'userPage/');
  bindButton('delete-profile-button', 'deleteProfile/');

  const editProfileButton = document.getElementById('edit-profile-button');
  if (editProfileButton) {
    editProfileButton.addEventListener('click', function(event) {
      event.preventDefault();
      window.location.href = 'editProfile/';
    });
  }

});