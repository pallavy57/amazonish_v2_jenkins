$(document).ready(() => {
    var myHTMLs = [];
    var newArr = null
    function removeDuplicates(arr) {

        const ids = arr.map(({ id }) => id);
        const filtered = arr.filter(({ id }, index) =>
            !ids.includes(id, index + 1));
        return filtered

    }

    const addHtml = (res, ids, myHTMLs) => {
        var i = 0;
        while (i < res.length) {
            var html = `<div class="card">
       <div class="imgBox">
         <img src="data:image/jpeg;base64,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" alt="mouse corsair" class="mouse">
       </div>
     
       <div class="contentBox">
         <h3>${res[i].fields.title}</h3>
         <h2 class="price">61.<small>98</small> €</h2>
         <a href="#" class="buy">Buy Now</a>
       </div>
     </div`
            myHTMLs.push({ html: html, id: res[i].pk });
            newArr = removeDuplicates(myHTMLs)
            i++;
        }

        newArr?.map(ite => {
            console.log("triggerinf");
            $('#showProducts').prepend(ite.html);
        })
    }

    const pushLatestElement = (resLast) => {
        console.log(resLast);
        var html = `<div class="card">
       <div class="imgBox">
         <img src="data:image/jpeg;base64,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" alt="mouse corsair" class="mouse">
       </div>
     
       <div class="contentBox">
         <h3>${resLast.fields.title}</h3>
         <h2 class="price">61.<small>98</small> €</h2>
         <a href="#" class="buy">Buy Now</a>
       </div>
     </div`

        myHTMLs.push({ html: html, id: resLast.pk });
        newArr = removeDuplicates(myHTMLs)
        $('#showProducts').prepend(html);
    }

    const refreshLogic = (res) => {

        const ids = res.map(r => {
            return r.pk
        });
        if (myHTMLs.length == 0) {
            addHtml(res, ids, myHTMLs)
        }

        const htmlIds = myHTMLs?.map(r => {
            return r.id
        });

        if (myHTMLs.length > 0) {
            ids.map(item => {
                if (!htmlIds.includes(item)) {
                    console.log(item, htmlIds)
                    pushLatestElement(res[res.length - 1])
                }
            })
        }
    }


    const getProducts = () => {
        $.ajax({
            url: '/tasks/',
            data: { type: 0 },
            method: 'POST',
        })
            .done((res) => {

                refreshLogic(res)
                setTimeout(() => {
                    getProducts()
                }, 1000);

            })
            .fail((err) => {
                console.log(err);
            });





    }

    if (newArr == null) {
        getProducts();
    }



});