-- version: 0.1.0
BEGIN;
DO $$ BEGIN CREATE TYPE resolution__enum AS ENUM (
    'P1D',
    'P7D',
    'PT1M',
    'PT2M',
    'PT5M',
    'PT15M',
    'PT30M',
    'PT60M'
);
EXCEPTION
WHEN duplicate_object THEN null;
END $$;
-- stock_values
CREATE TABLE IF NOT EXISTS stock_values (
    id SERIAL PRIMARY KEY,
    symbol character varying(64) NOT NULL,
    time timestamp NOT NULL,
    resolution resolution__enum,
    o numeric DEFAULT NULL,
    h numeric DEFAULT NULL,
    l numeric DEFAULT NULL,
    c numeric DEFAULT NULL,
    v numeric DEFAULT NULL,
    UNIQUE (symbol, time, resolution)
);
CREATE INDEX IF NOT EXISTS idx__stock_values__time ON stock_values(time);
-- stock_indicators_bbands
CREATE TABLE IF NOT EXISTS stock_indicators_bbands (
    id SERIAL PRIMARY KEY,
    symbol character varying(64) NOT NULL,
    time timestamp NOT NULL,
    resolution resolution__enum,
    timeperiod integer,
    nbdevup integer,
    nbdevdn integer,
    matype integer,
    u numeric DEFAULT NULL,
    m numeric DEFAULT NULL,
    l numeric DEFAULT NULL,
    UNIQUE (symbol, time, resolution)
);
CREATE INDEX IF NOT EXISTS idx__stock_indicators_bbands__time ON stock_values(time);
-- stock_indicators_macd
CREATE TABLE IF NOT EXISTS stock_indicators_macd (
    id SERIAL PRIMARY KEY,
    symbol character varying(64) NOT NULL,
    time timestamp NOT NULL,
    resolution resolution__enum,
    fastperiod integer,
    slowperiod integer,
    signalperiod integer,
    m numeric DEFAULT NULL,
    ms numeric DEFAULT NULL,
    mh numeric DEFAULT NULL,
    UNIQUE (symbol, time, resolution)
);
CREATE INDEX IF NOT EXISTS idx__stock_indicators_macd__time ON stock_values(time);
-- stock_indicators_rsi
CREATE TABLE IF NOT EXISTS stock_indicators_rsi (
    id SERIAL PRIMARY KEY,
    symbol character varying(64) NOT NULL,
    time timestamp NOT NULL,
    resolution resolution__enum,
    timeperiod integer,
    r numeric DEFAULT NULL,
    UNIQUE (symbol, time, resolution)
);
CREATE INDEX IF NOT EXISTS idx__stock_indicators_rsi__time ON stock_values(time);
COMMIT;