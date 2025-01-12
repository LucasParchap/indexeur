import { EvmBatchProcessor } from '@subsquid/evm-processor';
import { TypeormDatabase } from '@subsquid/typeorm-store';
import * as usdtAbi from './abi/usdt'; // ABI générée par squid-evm-typegen
import { Token, Transfer, TokenBalance, Metric } from './model';
import { Contract } from './abi/usdt'; // Classe Contract générée par squid-evm-typegen
import { Not } from 'typeorm';
import 'dotenv/config';

const USDT_CONTRACT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7';

const processor = new EvmBatchProcessor()
    .setGateway('https://v2.archive.subsquid.io/network/ethereum-mainnet')
    .setRpcEndpoint({
        url: process.env.RPC_ETH_HTTP,
        rateLimit: 20,
    })
    .setFinalityConfirmation(15)
    .addLog({
        address: [USDT_CONTRACT_ADDRESS],
        topic0: [usdtAbi.events.Transfer.topic],
    });

const db = new TypeormDatabase();

processor.run(db, async (ctx) => {
    console.log(`Début du traitement`);
    const transfers: Transfer[] = [];
    let metrics = await ctx.store.findOne(Metric, { where: { id: 'global-metrics' } });

    if (!metrics) {
        metrics = new Metric({
            id: 'global-metrics',
            totalTransfers: 0,
            totalHolders: 0,
        });
    }

    for (let block of ctx.blocks) {
        console.log(`Traitement du bloc ${block.header.height}`);
        const usdtContract = new Contract(ctx, block.header, USDT_CONTRACT_ADDRESS);

        for (let log of block.logs) {
            const { from, to, value } = usdtAbi.events.Transfer.decode(log);
            console.log(`Transfert trouvé : ${log.id}`);

            let token = await ctx.store.findOne(Token, { where: { id: USDT_CONTRACT_ADDRESS } });
            if (!token) {
                try {

                    const name = await usdtContract.name();
                    const symbol = await usdtContract.symbol();
                    const decimals = await usdtContract.decimals();
                    const totalSupply = await usdtContract.totalSupply();

                    token = new Token({
                        id: USDT_CONTRACT_ADDRESS,
                        name,
                        symbol,
                        decimals: Number(decimals),
                        totalSupply: BigInt(totalSupply.toString()),
                    });

                    await ctx.store.save(token);
                } catch (error) {
                    ctx.log.error(`Erreur lors de la récupération des métadonnées du token : ${error}`);
                    continue;
                }
            }

            transfers.push(
                new Transfer({
                    id: log.id,
                    from,
                    to,
                    value: BigInt(value.toString()),
                })
            );

            for (const address of [from, to]) {
                const balanceId = `${address}-${USDT_CONTRACT_ADDRESS}`;
                let balance = await ctx.store.findOne(TokenBalance, { where: { id: balanceId } });

                if (!balance) {
                    try {
                        const balanceOf = await usdtContract.balanceOf(address);
                        balance = new TokenBalance({
                            id: balanceId,
                            owner: address,
                            token,
                            balance: BigInt(balanceOf.toString()),
                        });
                    } catch (error) {
                        ctx.log.error(`Erreur lors de la récupération du solde pour ${address}: ${error}`);
                        continue;
                    }
                }

                balance.balance += address === to ? BigInt(value.toString()) : -BigInt(value.toString());
                await ctx.store.save(balance);
            }
        }
    }

    metrics.totalTransfers += transfers.length;
    metrics.totalHolders = await ctx.store.count(TokenBalance, {
        where: { balance: Not(BigInt(0)) },
    });

    await ctx.store.save(metrics);
    await ctx.store.insert(transfers);
});
