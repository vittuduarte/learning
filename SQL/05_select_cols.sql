SELECT IdCliente,
        QtdePontos,
        QtdePontos + 10 AS QtdePontosPlus10,
        QtdePontos * 2 AS QtdePontosMult2,
        DtCriacao,
        substr(DtCriacao, 1, 10) AS subString,
        datetime(substr(DtCriacao, 1, 10)) AS dtCriacaoNova,
        strftime('%w', datetime(substr(DtCriacao, 1, 10))) AS diaSemana
FROM clientes