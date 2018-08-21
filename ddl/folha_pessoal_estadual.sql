DROP TABLE IF EXISTS folha_pessoal_estadual;
CREATE TABLE folha_pessoal_estadual (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  de_poder TEXT,
  de_OrgaoLotacao TEXT,
  no_cargo TEXT,
  tp_cargo TEXT,
  nu_cpf VARCHAR(11),
  no_Servidor TEXT,
  dt_mesano VARCHAR(6),
  dt_Admissao DATE,
  vl_vantagens NUMERIC(12,4)
);
