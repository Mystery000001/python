function handle(){

	$("button[event=detail]").on("click", (e)=>{

        let detailView =  {
            el: "#detailShow",
            url: "/marks/salLogs/show/",
            method: "GET",
            where: {
                salId: $(e.target).attr("data"),
            },
            page: false,
            cols: [
                {
                    field: "goodId",
                    title: "商品编号",
                    align: "center",
                },
                {
                    field: "goodName",
                    title: "商品名称",
                    align: "center",
                },
                {
                    field: "nowPrice",
                    title: "商品现价",
                    align: "center",
                },
                {
                    field: "salPrice",
                    title: "商品售价",
                    align: "center",
                },
                {
                    field: "salTotal",
                    title: "销售数目",
                    align: "center",
                }
            ],
            binds: (d) =>{

            }
        }
        $.table(detailView);
        $.model(".detailWin");
    });
}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/marks/sals/page/",
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
				field: "salTotal",
				title: "销售总额",
				align: "center",
			},
			{
				field: "discount",
				title: "折扣力度",
				align: "center",
			},
			{
				field: "payTotal",
				title: "实付费用",
				align: "center",
			},
			{
				field: "member",
				title: "会员账号",
				align: "center",
			},
			{
				field: "createTime",
				title: "记录时间",
				align: "center",
			},
			{
                title: "操作",
                template: (d)=>{

                    return `
                            <button type="button" event="detail" data="${d.id}" class="fater-btn fater-btn-primary fater-btn-sm">
                                详情
                            </button>
                            `;
                }
            }
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);

    $(".fater-btn-form-qry").on("click", ()=>{

        tableView.where["member"] = $("[name=para1]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addSalBtn").on("click", (e)=>{

        $(".fater-sal").append(
                                    `
                                    <div class="fater-sal-form">
                                        <div class="fater-sal-item">
                                            <label>商品编号</label>
                                            <input type="text" name="gooId" placeholder="请输入商品编号……"/>
                                        </div>
                                        <div class="fater-sal-item">
                                            <label>购买数目</label>
                                            <input type="text" name="gooTotal" placeholder="请输入购买数目……"/>
                                        </div>
                                        <div class="fater-sal-item">
                                            <span event="delRow" class="fa fa-minus-circle"></span>
                                        </div>
                                    </div>
                                    `
                                    );

        $("span[event=delRow]").on("click", (e)=>{

            $(e.target).parent().parent().remove();
        });
    });

    $("#addFormBtn").on("click", (e)=>{

        let goodIds = [];
        let goodTotals = [];

        $.each($(".fater-sal-form").find("input[name=gooId]"), (index, item) =>{

			goodIds.push($(item).val());
		});

		$.each($(".fater-sal-form").find("input[name=gooTotal]"), (index, item) =>{

			goodTotals.push(parseFloat($(item).val()));
		});

        $.ajax({
            url: "/marks/sals/add/",
            type: "POST",
            data: {
                memberId: $("#memberId").val(),
                goodIds: goodIds,
                goodTotals: goodTotals
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