var allLabelData = []
var index = -1;
var labelData = []

$(function () {
    var start_date = new Date();
    var start_unix_time = start_date.getTime() / 1000;
    for (let i = 0; i < outer_data.length; i++) {
        allLabelData.push(outer_data[i]);
    }
    //console.log(allLabelData);
    let last_idx = outer_data[outer_data.length - 1][0];
    index = last_idx + 1;
    $("button.btn").on("click", getSelectedRange);
    $("button.btn").on("click", getButtonName);
    $("button.label-button").on("click", storeData);

    function getSelectedRange() {
        var selection = window.getSelection();
        var range = selection.getRangeAt(0);
        var prerange = range.cloneRange();
        var parents = $(range).parents("div.border-line");
        var search = $(range).parents("div.border-line").find('#selectable-text');
        var correct = $("#selectable-text")


        console.log("start")
        console.log(labelData);

        var sentence = document.getElementsByClassName("edit-table").item(0);
        prerange.setStart(sentence, 0);

        prerange.setEnd(range.startContainer, range.startOffset);
        start = prerange.toString().length;
        end = start + range.toString().length;
        word = window.getSelection().toString();


        if (start !== end) {
            labelData = [];
            labelData.push(index);
            index++;
            labelData.push(word);
            labelData.push(start);
            labelData.push(end);
        } else {
            start = -1;
            end = -1;
            word = "";
        }
    }

    function getButtonName() {
        labelName = $(this).text();
        var statButton = $("input[name=group1]:eq(1)").is(":checked");
        if (statButton == true) {
            labelName += "-question";
        }
        labelData.push(labelName);

    }

    function storeData() {
        console.log("labelData: ", labelData);
        if (labelData.length == 5) {
            allLabelData.push(labelData);
            console.log("AlllabelData: ", allLabelData);

        }

    }
    $("button.label-button").on("click", addSpanTag);
    function addSpanTag() {
        if (labelData.length == 5) {
            var selection = window.getSelection();
            var range = selection.getRangeAt(0);

            var span = document.createElement("span");
            let labelName = $(this).text();
            span.setAttribute("class", labelName);
            span.textContent = selection.toString();
            var data_index = index - 1;
            var delete_button =
                '<button class="delete btn btn-dark btn-sm" data-id=' +
                data_index +
                ">" +
                '<i class="fa fa-close">' +
                "</button>";
            $(span).append(delete_button);
            range.deleteContents();
            range.insertNode(span);
            window.getSelection().empty(); //解除
        }
        labelData = [];
    }

    $(document).on("keyup", (event) => {
        var t = $("span.keybind");
        for (let i = 0; i < t.length; i++) {
            let tmp = t.eq(i);
            let tmpText = tmp.text();
            if (event.key == tmpText) {
                var labelName = t.eq(i).prev().text();


                getSelectedRange();
                labelData.push(labelName);
                storeData();
                var selection = window.getSelection();
                var range = selection.getRangeAt(0);

                var span = document.createElement("span");
                span.setAttribute("class", labelName);
                span.textContent = selection.toString();

                var data_index = index - 1;
                var delete_button =
                    '<button class="delete btn btn-dark btn-sm" data-id=' +
                    data_index +
                    ">" +
                    '<i class="fa fa-close">' +
                    "</button>";
                if (labelData.length == 5) {
                    $(span).append(delete_button);
                    range.deleteContents();
                    range.insertNode(span);
                }
                window.getSelection().empty(); //解除
                window.getSelection().empty(); //解除
                break;
            }
        }
        labelData = [];
    });

    $(".text").on("click", "button.delete", function () {
        var tmp_span = $(this).parent();
        let data_index = $(this).data("id");


        //index で検索して消去
        let target = allLabelData.find((array) => array[0] == data_index);
        allLabelData.some(function (value, index) {
            if (value == target) {
                allLabelData.splice(index, 1);
            }
        });

        $(this).remove();
        tmp_span.contents().unwrap();
    });
    $("input.data-submit").on("click", () => {
        var result = window.confirm("提出してよろしいでしょうか?");
        if (result) {
            let text = $("text").text();
            console.log("allDAta: ", allLabelData);
            var str_all_data = '';
            for (var i = 0; i < allLabelData.length; i++) {
                str_data = allLabelData[i].join(',');
                str_data = str_data + '\t';
                str_all_data += str_data
            }
            document.getElementById('target').value = str_all_data;

            if (str_all_data.length < 1) {
                console.log("length");
                console.log(str_all_data.length)
                str_all_data = 'ALL_Os'
                document.getElementById('target').value = str_all_data;
            }
            console.log('str_all_data: ', str_all_data);

            var end_date = new Date();
            var end_unix_time = end_date.getTime() / 1000;

            document.getElementById('start_time').value = start_unix_time;
            document.getElementById('end_time').value = end_unix_time;

        } else {
            return false; //POST is stopped.
        }
    });
    var labelButtons = $("button.label-button");
    //var labelColors = $(".labelColor");

    for (let i = 0; i < labelButtons.length; i++) {
        let labelButton = labelButtons.eq(i);
        let color = labelButton.css('background-color');


        var head = document.getElementsByTagName("head").item(0);
        var style = document.createElement("style");
        var style2 = document.createElement("style");
        var text =
            "." +
            labelButton.text() +
            " {background-color: " +
            color +
            ";}";
        var text_question =
            "." +
            labelButton.text() +
            "-question" +
            " {background-color: " +
            color +
            ";}";
        var rule = document.createTextNode(text);
        var rule2 = document.createTextNode(text_question);
        style.media = "screen";
        style2.media = "screen";
        style.type = "text/css";
        style2.type = "text/css";
        style.appendChild(rule);
        style2.appendChild(rule2);
        head.appendChild(style);
        head.appendChild(style2);


    }
})