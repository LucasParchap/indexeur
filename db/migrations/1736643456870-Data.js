module.exports = class Data1736643456870 {
    name = 'Data1736643456870'

    async up(db) {
        await db.query(`CREATE TABLE "transfer" ("id" character varying NOT NULL, "from" text NOT NULL, "to" text NOT NULL, "value" numeric NOT NULL, CONSTRAINT "PK_fd9ddbdd49a17afcbe014401295" PRIMARY KEY ("id"))`)
        await db.query(`CREATE INDEX "IDX_be54ea276e0f665ffc38630fc0" ON "transfer" ("from") `)
        await db.query(`CREATE INDEX "IDX_4cbc37e8c3b47ded161f44c24f" ON "transfer" ("to") `)
        await db.query(`CREATE TABLE "token" ("id" character varying NOT NULL, "name" text NOT NULL, "symbol" text NOT NULL, "decimals" integer NOT NULL, "total_supply" numeric NOT NULL, CONSTRAINT "PK_82fae97f905930df5d62a702fc9" PRIMARY KEY ("id"))`)
        await db.query(`CREATE TABLE "token_balance" ("id" character varying NOT NULL, "owner" text NOT NULL, "balance" numeric NOT NULL, "token_id" character varying, CONSTRAINT "PK_dc23ea262a0188977523d90ae7f" PRIMARY KEY ("id"))`)
        await db.query(`CREATE INDEX "IDX_e00189bbd79edf72f941e4358a" ON "token_balance" ("owner") `)
        await db.query(`CREATE INDEX "IDX_5813c3040e74c285719679c693" ON "token_balance" ("token_id") `)
        await db.query(`CREATE TABLE "metric" ("id" character varying NOT NULL, "total_transfers" integer NOT NULL, "total_holders" integer NOT NULL, CONSTRAINT "PK_7d24c075ea2926dd32bd1c534ce" PRIMARY KEY ("id"))`)
        await db.query(`ALTER TABLE "token_balance" ADD CONSTRAINT "FK_5813c3040e74c285719679c6935" FOREIGN KEY ("token_id") REFERENCES "token"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`)
    }

    async down(db) {
        await db.query(`DROP TABLE "transfer"`)
        await db.query(`DROP INDEX "public"."IDX_be54ea276e0f665ffc38630fc0"`)
        await db.query(`DROP INDEX "public"."IDX_4cbc37e8c3b47ded161f44c24f"`)
        await db.query(`DROP TABLE "token"`)
        await db.query(`DROP TABLE "token_balance"`)
        await db.query(`DROP INDEX "public"."IDX_e00189bbd79edf72f941e4358a"`)
        await db.query(`DROP INDEX "public"."IDX_5813c3040e74c285719679c693"`)
        await db.query(`DROP TABLE "metric"`)
        await db.query(`ALTER TABLE "token_balance" DROP CONSTRAINT "FK_5813c3040e74c285719679c6935"`)
    }
}
