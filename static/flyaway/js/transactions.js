

// Esews

var path="https://uat.esewa.com.np/epay/main";
var params= {
    amt: 100,
    psc: 0,
    pdc: 0,
    txAmt: 0,
    tAmt: 100,
    pid: "ee2c3ca1-696b-4cc5-a6be-2c40d929d453",
    scd: "EPAYTEST",
    su: "http://merchant.com.np/page/esewa_payment_success",
    fu: "http://merchant.com.np/page/esewa_payment_failed"
}

function post(path, params) {
    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", path);

    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);
        form.appendChild(hiddenField);
    }

    document.body.appendChild(form);
    form.submit();
}
// ends here


// // Khalti App

//     var config = {
//         // replace the publicKey with yours
//         "publicKey": "test_public_key_dc74e0fd57cb46cd93832aee0a390234",
//         "productIdentity": "1234567890",
//         "productName": "Dragon",
//         "productUrl": "http://gameofthrones.wikia.com/wiki/Dragons",
//         "paymentPreference": [
//             "KHALTI",
//             "EBANKING",
//             "MOBILE_BANKING",
//             "CONNECT_IPS",
//             "SCT",
//             ],
//         "eventHandler": {
//             onSuccess (payload) {
//                 // hit merchant api for initiating verfication
//                 console.log(payload);
//             },
//             onError (error) {
//                 console.log(error);
//             },
//             onClose () {
//                 console.log('widget is closing');
//             }
//         }
//     };

//     var checkout = new KhaltiCheckout(config);
//     var btn = document.getElementById("payment-button");
//     btn.onclick = function () {
//         // minimum transaction amount must be 10, i.e 1000 in paisa.
//         checkout.show({amount: 1000});
//     }

// //  Khalti Appp ends here



