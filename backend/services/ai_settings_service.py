from typing import List, Dict, Optional
from services.database_service import DatabaseService


class AISettingsService:
    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_settings(self) -> List[Dict]:
        """Get all AI provider settings"""
        conn = None
        cur = None
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            query = """
                SELECT provider, enabled, model_version, updated_at
                FROM ai_settings
                ORDER BY provider
            """
            cur.execute(query)
            rows = cur.fetchall()
            
            # Manually build dictionaries from rows
            settings = []
            for row in rows:
                settings.append({
                    'provider': row[0],
                    'enabled': bool(row[1]),
                    'model_version': row[2],
                    'updated_at': row[3]
                })
            
            return settings
            
        except Exception as e:
            print(f"Error getting AI settings: {e}")
            return []
        finally:
            self.db_service.close_resources(cur, conn)

    def get_setting(self, provider: str) -> Optional[Dict]:
        """Get settings for a specific AI provider"""
        conn = None
        cur = None
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            query = """
                SELECT provider, enabled, model_version, updated_at
                FROM ai_settings
                WHERE provider = ?
            """
            cur.execute(query, (provider,))
            row = cur.fetchone()
            
            if row:
                return {
                    'provider': row[0],
                    'enabled': bool(row[1]),
                    'model_version': row[2],
                    'updated_at': row[3]
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting AI setting for {provider}: {e}")
            return None
        finally:
            self.db_service.close_resources(cur, conn)

    def update_setting(self, provider: str, enabled: Optional[bool] = None, 
                       model_version: Optional[str] = None) -> bool:
        """Update settings for a specific AI provider"""
        conn = None
        cur = None
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            # Build dynamic update query based on provided parameters
            update_parts = []
            params = []
            
            if enabled is not None:
                update_parts.append("enabled = ?")
                params.append(1 if enabled else 0)
            
            if model_version is not None:
                update_parts.append("model_version = ?")
                params.append(model_version)
            
            if not update_parts:
                return False
            
            params.append(provider)
            params_tuple = tuple(params)
            
            query = f"""
                UPDATE ai_settings
                SET {', '.join(update_parts)}
                WHERE provider = ?
            """
            
            cur.execute(query, params_tuple)
            conn.commit()
            
            # Return True as long as the query executed without error
            # rowcount might be 0 if the value didn't actually change
            return True
            
        except Exception as e:
            print(f"Error updating AI setting for {provider}: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            self.db_service.close_resources(cur, conn)

    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a specific AI provider is enabled"""
        setting = self.get_setting(provider)
        return setting['enabled'] if setting else False

    def get_enabled_providers(self) -> List[str]:
        """Get list of all enabled AI providers"""
        all_settings = self.get_all_settings()
        return [s['provider'] for s in all_settings if s['enabled']]

    def get_provider_model(self, provider: str) -> Optional[str]:
        """Get the current model version for a provider"""
        setting = self.get_setting(provider)
        return setting['model_version'] if setting else None
