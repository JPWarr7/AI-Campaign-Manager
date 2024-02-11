from app.database import execute_query


def broker_stocks(bkr_id):
    statement = """
        select S.stk_id, S.name, S.code 
            from stocks as S
            join stock_brokers as B using (stk_id)
            where B.bkr_id = %(bkr_id)s
    """
    data = {"bkr_id": bkr_id}
    return execute_query(statement, data, many=True)


def trader_stocks(tdr_id):
    statement = """
        select distinct S.stk_id, S.name, S.code
            from stocks as S
            join stock_brokers as B using (stk_id)
            join shares as H using (stb_id)
            where H.tdr_id = %(tdr_id)s
    """
    data = {"tdr_id": tdr_id}
    return execute_query(statement, data, many=True)


def stocks_query():
    statement = """
        select * from stocks as S
    """
    return execute_query(statement, many=True)


def stock_info_query(stk_id):
    statement = """
       with
        available_shares as (
            select S.stk_id, HA.quantity as available
                from stocks as S
                join stock_brokers using (stk_id)
                join shares as H using (stb_id)
                join share_amounts as HA using (shr_id)
                where H.tdr_id is null
        )
        select S.name, S.code,
            sum(HA.quantity) as total_count,
            sum(available) as unowned_count
            from stocks as S
            join stock_brokers using (stk_id)
            join shares using (stb_id)
            join available_shares using (stk_id)
            join share_amounts as HA using (shr_id)
            where S.stk_id = %(stk_id)s
            group by S.stk_id;
    """
    data = {"stk_id": stk_id}
    return execute_query(statement, data)


def stock_broker_query(stk_id, tdr_id=None):
    statement = """
        with
        share_counts as (
            select SH.stb_id, sum(SHA.quantity) as shares_owned
                from share_amounts as SHA
                join shares as SH using (shr_id)
                group by SH.stb_id
        ),
        available_counts as (
            select SH.stb_id, sum(SHA.quantity) as shares_available
                from share_amounts as SHA
                join shares as SH using (shr_id)
                where if(isnull(%(tdr_id)s), SH.tdr_id is null, SH.tdr_id = %(tdr_id)s)
                group by SH.stb_id
        )
        select U.usr_id, U.first_name, U.last_name, U.username, shares_owned, shares_available
            from v_brokers as U
            join stock_brokers as SB on U.usr_id = SB.bkr_id
            join stocks as ST using (stk_id)
            join share_counts using (stb_id)
            join available_counts using (stb_id)
            where SB.stk_id = %(stk_id)s
            order by usr_id;
    """
    data = {"stk_id": stk_id, "tdr_id": tdr_id}
    return execute_query(statement, data, many=True)


def create_stock(bkr_id, name, code):
    statement = """
        call create_stock(%(bkr_id)s, %(name)s, %(code)s);
    """
    data = {
        "bkr_id": bkr_id,
        "name": name,
        "code": code
    }
    print(bkr_id, name, code)
    return execute_query(statement, data, action="write")


def delist_stock(stk_id):
    statement = """
        select delistStock(%(stk_id)s)
    """
    data = {"stk_id": stk_id}
    return execute_query(statement, data, action="write")


def stock_history(stk_id):
    statement = """
        call view_requests(null, null, %(stk_id)s, null);
    """
    data = {"stk_id": stk_id}
    return execute_query(statement, data, many=True)
