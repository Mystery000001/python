function handle(){

	$("button[event=upd]").on("click", (e)=>{

        $.ajax({
            url: "/marks/users/info/",
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

    $("button[event=del]").on("click", (e)=>{

        $.confirm("确认要删除吗", () =>{

            $.ajax({
                url: "/marks/users/del/",
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
        url: "/marks/users/page/",
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
				field: "userName",
				title: "用户账号",
				align: "center",
			},
			{
				field: "name",
				title: "用户姓名",
				align: "center",
			},
			{
				field: "gender",
				title: "用户性别",
				align: "center",
			},
			{
				field: "age",
				title: "用户年龄",
				align: "center",
			},
			{
				field: "phone",
				title: "联系电话",
				align: "center",
			},
			{
				field: "address",
				title: "联系地址",
				align: "center",
			},
			{
				title: "用户账号",
				template: (d)=>{

				    if(d.type == 0){

				        return "管理员"
				    }
				    if(d.type == 1){

				        return "销售员"
				    }
				    if(d.type == 2){

				        return "采购员"
				    }
				}
			},
			{
                title: "操作",
                template: (d)=>{

                    if(d.type == 0){

				        return `
                            <button type="button" class="fater-btn fater-btn-disableed fater-btn-sm">
                                <span class="fa fa-edit"></span>
                            </button>
                            <button type="button" class="fater-btn fater-btn-disableed fater-btn-sm">
                                <span class="fa fa-trash"></span>
                            </button>
                            `;
				    }else{

				        return `
                            <button type="button" event="upd" data="${d.id}" class="fater-btn fater-btn-primary fater-btn-sm">
                                <span data="${d.id}" class="fa fa-edit"></span>
                            </button>
                            <button type="button" event="del" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.id}" class="fa fa-trash"></span>
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

        tableView.where["userName"] = $("[name=para1]").val();
        tableView.where["name"] = $("[name=para2]").val();
        tableView.where["phone"] = $("[name=para3]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addFormBtn").on("click", ()=>{

        let formVal = $.getFrom("addForm");

        $.ajax({
            url: "/marks/users/add/",
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
            url: "/marks/users/upd/",
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