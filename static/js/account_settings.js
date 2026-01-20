const profileInput = document.getElementById("id_profile_pic");
const profileImage = document.getElementById("profileImage");
const defaultImage = profileImage.dataset.defaultSrc;

// Preview image when selected
profileInput.addEventListener("change", function () {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        profileImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
});

// Remove photo button
const removeBtn = document.getElementById("removePhotoBtn");
if (removeBtn) {
    removeBtn.addEventListener("click", function () {
        const checkbox = document.getElementById("id_profile_pic_clear");
        if (checkbox) checkbox.checked = true;

        // Reset to default image safely
        profileImage.src = defaultImage;
    });
}
