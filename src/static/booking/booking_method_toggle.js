function showTimeMethodField() {
    document.getElementById('id_earliest_depart_time').parentNode.parentNode.parentNode.style.display = 'block';
    document.getElementById('id_latest_arrival_time').parentNode.parentNode.parentNode.style.display = 'block';
    document.getElementById('id_train_id').parentNode.parentNode.parentNode.style.display = 'none';
}

function showTrainNoMethodField() {
    document.getElementById('id_earliest_depart_time').parentNode.parentNode.parentNode.style.display = 'none';
    document.getElementById('id_latest_arrival_time').parentNode.parentNode.parentNode.style.display = 'none';
    document.getElementById('id_train_id').parentNode.parentNode.parentNode.style.display = 'block';
}

function toggleFields() {
    let bookingMethod = document.getElementById('id_booking_method').value;
    if (bookingMethod == '0') { // BookingMethod.TIME
        showTimeMethodField();
    } else if (bookingMethod == '1') { // BookingMethod.TRAIN_NO
        showTrainNoMethodField();
    }
}
window.onload = function() {
    toggleFields();

    document.getElementById('id_booking_method').addEventListener('change', toggleFields);
}