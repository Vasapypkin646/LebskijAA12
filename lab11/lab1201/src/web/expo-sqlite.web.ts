// Заглушка для SQLite на вебе
// Использует in-memory хранилище для тестирования

interface Note {
    id: string;
    title: string;
    content: string;
    latitude: number;
    longitude: number;
    address?: string;
    photoUri?: string;
    createdAt: number;
}

// In-memory storage для веба
const memoryStore: Note[] = [];

export const openDatabaseSync = (name: string) => {
    console.warn(`SQLite is not supported on web. Using in-memory storage for: ${name}`);
    
    return {
        execAsync: async (sql: string) => {
            console.log('execAsync:', sql);
            return [];
        },
        
        getAllAsync: async (sql: string, params?: any[]) => {
            console.log('getAllAsync:', sql, params);
            // Простой парсинг SQL для получения данных
            if (sql.includes('SELECT * FROM notes')) {
                return [...memoryStore].sort((a, b) => b.createdAt - a.createdAt);
            }
            return [];
        },
        
        runAsync: async (sql: string, params?: any[]) => {
            console.log('runAsync:', sql, params);
            
            // INSERT
            if (sql.includes('INSERT INTO notes')) {
                if (params && params[0]) {
                    const newNote: Note = {
                        id: params[0],
                        title: params[1],
                        content: params[2],
                        latitude: params[3],
                        longitude: params[4],
                        address: params[5],
                        photoUri: params[6],
                        createdAt: params[7]
                    };
                    memoryStore.push(newNote);
                }
            }
            
            // DELETE
            if (sql.includes('DELETE FROM notes')) {
                if (params && params[0]) {
                    const index = memoryStore.findIndex(n => n.id === params[0]);
                    if (index !== -1) {
                        memoryStore.splice(index, 1);
                    }
                }
            }
            
            // UPDATE
            if (sql.includes('UPDATE notes')) {
                if (params) {
                    const index = memoryStore.findIndex(n => n.id === params[4]);
                    if (index !== -1) {
                        memoryStore[index] = {
                            ...memoryStore[index],
                            title: params[0],
                            content: params[1],
                            address: params[2],
                            photoUri: params[3]
                        };
                    }
                }
            }
            
            return { rowsAffected: 1 };
        },
        
        getFirstAsync: async (sql: string, params?: any[]) => {
            console.log('getFirstAsync:', sql, params);
            if (sql.includes('SELECT * FROM notes WHERE id = ?')) {
                if (params && params[0]) {
                    const note = memoryStore.find(n => n.id === params[0]);
                    return note || null;
                }
            }
            return null;
        }
    };
};

export default { openDatabaseSync };
