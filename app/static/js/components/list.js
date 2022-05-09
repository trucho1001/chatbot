function createList(list_data) {
    // sample data format:
    // var collapsible_data=[{"title":"abc","description":"xyz"},{"title":"pqr","description":"jkl"}]
    let List_list = "";
    for (let i = 0; i < list_data.length; i += 1) {
        const List_item = `<li>&nbsp&nbsp&nbsp&nbsp&#9830&nbsp${list_data[i].title}: ${list_data[i].description}</li>`;
        List_list += List_item;
    }
    const list_contents = `<ul class="listShow">${List_list}</ul>`;
    $(list_contents).appendTo(".chats");

    // initialize the collapsible
    // $(".listShow").listShow();
    scrollToBottomOfResults();
}
