var button = document.getElementsByClassName('update-cart')

for (i = 0; i < button.length; i++) {
    button[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("productId", productId, "action", action)
        console.log("user name ", user)

        if (user == "AnonymousUser") {
            updateCookieItem(productId, action)

        }
        else {
            updateCart(productId, action)
        }
    })

}
function updateCookieItem(productId, action) {
    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }
    if (action == "remove") {
        cart[productId]["quantity"] -= 1
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    console.log("cart", cart);
    location.reload();

}

function updateCart(productId, action) {
    console.log(productId)
    console.log(action)

    const data = {
        "productId": productId,
        "action": action
    }


    var requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data),
        redirect: 'follow',
    }
        ;

    fetch("http://127.0.0.1:8000/update_Item/", requestOptions,)
        .then(response => response.json())
        .then(result => console.log("result", result),
            location.reload()
        )
        .catch(error => console.log('error', error));
}