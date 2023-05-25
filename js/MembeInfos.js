function handle(){

	$("button[event=upd]").on("click", (e)=>{

        $.ajax({
            url: "/marks/memberInfos/info/",
            type: "GET",
            async: false,
            data:{
                phone: $(e.target).attr("data"),
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
                url: "/marks/memberInfos/del/",
                type: "POST",
                async: false,
                data:{
                    phone: $(e.target).attr("data"),
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
        url: "/marks/memberInfos/page/",
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
				field: "phone",
				title: "会员账号",
				align: "center",
			},
			{
				field: "levelName",
				title: "会员等级",
				align: "center",
			},
			{
				field: "total",
				title: "消费额度",
				align: "center",
			},
			{
				field: "createTime",
				title: "注册时间",
				align: "center",
			},
			{
                title: "操作",
                template: (d)=>{

                    if($("#sessionUserType").val() == 0){

                        return `
                            <button type="button" event="upd" data="${d.phone}" class="fater-btn fater-btn-primary fater-btn-sm">
                                <span data="${d.phone}" class="fa fa-edit"></span>
                            </button>
                            <button type="button" event="del" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.phone}" class="fa fa-trash"></span>
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

        tableView.where["phone"] = $("[name=para1]").val();
        tableView.where["levelId"] = $("[name=para2]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addFormBtn").on("click", ()=>{

        let formVal = $.getFrom("addForm");

        $.ajax({
            url: "/marks/memberInfos/add/",
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
            url: "/marks/memberInfos/upd/",
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