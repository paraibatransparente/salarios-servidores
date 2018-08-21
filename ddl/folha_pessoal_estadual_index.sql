CREATE INDEX IF NOT EXISTS idx_folha_pessoal_de_poder ON folha_pessoal_estadual (de_poder);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_de_OrgaoLotacao ON folha_pessoal_estadual (de_OrgaoLotacao);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_no_cargo ON folha_pessoal_estadual (no_cargo);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_nu_cpf ON folha_pessoal_estadual (nu_cpf);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_no_Servidor ON folha_pessoal_estadual (no_Servidor);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_dt_mesano ON folha_pessoal_estadual (dt_mesano);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_vl_vantagens ON folha_pessoal_estadual (vl_vantagens);
CREATE INDEX IF NOT EXISTS idx_folha_pessoal_substr_dt_mesano ON folha_pessoal_estadual (substr(dt_mesano, 3, 4));

ALTER TABLE folha_pessoal_estadual ADD ds_link_poder VARCHAR(100);
ALTER TABLE folha_pessoal_estadual ADD ds_link_orgao VARCHAR(100);
ALTER TABLE folha_pessoal_estadual ADD ds_link_cargo VARCHAR(100);
ALTER TABLE folha_pessoal_estadual ADD ds_link_tipo_cargo VARCHAR(100);
