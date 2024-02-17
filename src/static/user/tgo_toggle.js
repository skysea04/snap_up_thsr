window.onload = function() {
    const $ = django.jQuery;
    let useTGOAccountButton = $("#id_use_tgo_account");
    let sameAsPersonalIDButton = $("#id_tgo_account_same_as_personal_id");
    let sameAsPersonalID = $("#id_tgo_account_same_as_personal_id").parent().parent();
    let TGOAccount = $("#id_tgo_account").parent().parent();

    function toggleSameAsPersonalID() {
        if (useTGOAccountButton.is(':checked')) {
            sameAsPersonalID.show();
        } else {
            sameAsPersonalID.hide();
        }
    }

    function toggleTGOAccount() {
        if (useTGOAccountButton.is(':checked') && sameAsPersonalIDButton.is(':not(:checked)')) {
            TGOAccount.show();
        } else {
            TGOAccount.hide();
        }
    }

    toggleSameAsPersonalID();
    toggleTGOAccount();
    useTGOAccountButton.change(toggleSameAsPersonalID);
    useTGOAccountButton.change(toggleTGOAccount);
    sameAsPersonalIDButton.change(toggleTGOAccount);
};