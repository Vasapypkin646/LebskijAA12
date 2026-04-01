import { GeoNote } from '../types';
import { Platform } from 'react-native';

let SQLite: any;

if (Platform.OS === 'web') {
    // На вебе используем заглушку
    SQLite = require('../web/expo-sqlite.web');
} else {
    // На нативных платформах используем реальный expo-sqlite
    SQLite = require('expo-sqlite');
}

const db = SQLite.openDatabaseSync('geonotes.db');

export const initDatabase = async (): Promise<void> => {
    try {
        await db.execAsync(`
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                address TEXT,
                photoUri TEXT,
                createdAt INTEGER NOT NULL
            );
        `);
        console.log('Database initialized');
    } catch (error) {
        console.error('Database initialization error:', error);
        throw error;
    }
};

export const getNotes = async (): Promise<GeoNote[]> => {
    try {
        const result = await db.getAllAsync('SELECT * FROM notes ORDER BY createdAt DESC');
        return result as GeoNote[];
    } catch (error) {
        console.error('Get notes error:', error);
        throw error;
    }
};

export const addNote = async (note: GeoNote): Promise<void> => {
    try {
        await db.runAsync(
            'INSERT INTO notes (id, title, content, latitude, longitude, address, photoUri, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            [note.id, note.title, note.content, note.latitude, note.longitude, note.address || null, note.photoUri || null, note.createdAt]
        );
        console.log('Note added:', note.id);
    } catch (error) {
        console.error('Add note error:', error);
        throw error;
    }
};

export const deleteNote = async (id: string): Promise<void> => {
    try {
        await db.runAsync('DELETE FROM notes WHERE id = ?', [id]);
        console.log('Note deleted:', id);
    } catch (error) {
        console.error('Delete note error:', error);
        throw error;
    }
};

export const updateNote = async (note: GeoNote): Promise<void> => {
    try {
        await db.runAsync(
            'UPDATE notes SET title = ?, content = ?, address = ?, photoUri = ? WHERE id = ?',
            [note.title, note.content, note.address || null, note.photoUri || null, note.id]
        );
        console.log('Note updated:', note.id);
    } catch (error) {
        console.error('Update note error:', error);
        throw error;
    }
};

export const getNoteById = async (id: string): Promise<GeoNote | null> => {
    try {
        const result = await db.getFirstAsync('SELECT * FROM notes WHERE id = ?', [id]);
        return result as GeoNote | null;
    } catch (error) {
        console.error('Get note by id error:', error);
        throw error;
    }
};
