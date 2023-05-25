function handle(){

    let resl = [];

	$("button[event=upd]").on("click", (e)=>{

        $.ajax({
            url: "/marks/goodInfos/info/",
            type: "GET",
            async: false,
            data:{
                id: $(e.target).attr("data"),
            },
            success: function(res){
                if(res.code == 0){

                    $.initForm("updForm", res.data);
                    $.model(".updWin");
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    $("button[event=buy]").on("click", (e)=>{

        resl.push($(e.target).attr("data"));

        console.log(resl);
    });

    $("button[event=del]").on("click", (e)=>{

        $.confirm("确认要删除吗", () =>{

            $.ajax({
                url: "/marks/goodInfos/del/",
                type: "POST",
                async: false,
                data:{
                    id: $(e.target).attr("data"),
                },
                success: function(res){
                    if(res.code == 0){
                        $.alert(res.msg, () =>{

                            window.location.reload();
                        });
                    }else{
                        $.msg("error", res.msg);
                    }
                }
            });
        });
    });
}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/marks/goodInfos/page/",
        method: "GET",
        where: {
            pageIndex: 1,
            pageSize: 10
        },
        page: true,
        cols: [
            {
                type: "number",
                title: "序号",
            },
			{
				field: "id",
				title: "商品编号",
				align: "center",
			},
			{
				field: "name",
				title: "商品名称",
				align: "center",
			},
			{
				field: "price",
				title: "商品价格",
				align: "center",
			},
			{
				field: "total",
				title: "商品库存",
				align: "center",
			},
			{
				field: "typeName",
				title: "商品类型",
				align: "center",
			},
			{
                title: "操作",
                template: (d)=>{

                    if($("#sessionUserType").val() == 0){

                        return `
                            <button type="button" event="upd" data="${d.id}" class="fater-btn fater-btn-primary fater-btn-sm">
                                <span data="${d.id}" class="fa fa-edit"></span>
                            </button>
                            <button type="button" event="del" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.id}" class="fa fa-trash"></span>
                            </button>
                            `;
                    }else{
                        return `
                            <button type="button" class="fater-btn fater-btn-disableed fater-btn-sm">
                                <span class="fa fa-edit"></span>
                            </button>
                            <button type="button" class="fater-btn fater-btn-disableed fater-btn-sm">
                                <span class="fa fa-trash"></span>
                            </button>
                            `;
                    }
                }
            }
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);

    $(".fater-btn-form-qry").on("click", ()=>{

        tableView.where["name"] = $("[name=para1]").val();
        tableView.where["typeId"] = $("[name=para2]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addFormBtn").on("click", ()=>{

        let formVal = $.getFrom("addForm");

        $.ajax({
            url: "/marks/goodInfos/add/",
            type: "POST",
            data: formVal,
            success: function(res){
                if(res.code == 0){
                    $.alert(res.msg, () =>{

                        window.location.reload();
                    });
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });

    $("#updFormBtn").on("click", ()=>{

        let formVal = $.getFrom("updForm");

        $.ajax({
            url: "/marks/goodInfos/upd/",
            type: "POST",
            data: formVal,
            success: function(res){
                if(res.code == 0){
                    $.alert(res.msg, () =>{

                        window.location.reload();
                    });
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });
});