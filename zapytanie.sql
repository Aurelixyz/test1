-- ==========================================
-- POBIERANIE SPRZĘTU DO PROFILU UŻYTKOWNIKA
-- ==========================================
-- name: select_user_equipment_laptopy
SELECT * FROM dbo.msprzet_LAPTOPY WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_monitory
SELECT * FROM dbo.msprzet_MONITORY WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_telefony
SELECT * FROM dbo.msprzet_TELEFONY WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_sluchawki
SELECT * FROM dbo.msprzet_SLUCHAWKI WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_karty_sim
SELECT * FROM dbo.msprzet_KARTY_SIM WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_router
SELECT * FROM dbo.msprzet_ROUTER WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_myszki
SELECT COUNT(*) as LICZBA FROM dbo.msprzet_MYSZKI WHERE [ID_UZYTKOWNIKA] = ?
-- end

-- name: select_user_equipment_klawiatury
SELECT COUNT(*) as LICZBA FROM dbo.msprzet_KLAWIATURY WHERE [ID_UZYTKOWNIKA] = ?
-- end