import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import { GeoNote } from '../types';
import * as database from '../utils/database';

// Асинхронные действия (thunks)
export const loadNotes = createAsyncThunk(
    'notes/loadNotes',
    async () => {
        const notes = await database.getNotes();
        return notes;
    }
);

export const saveNote = createAsyncThunk(
    'notes/saveNote',
    async (note: GeoNote) => {
        // TODO: Реализовать сохранение в БД
        await database.addNote(note);
        return note;
    }
);

export const removeNote = createAsyncThunk(
    'notes/removeNote',
    async (id: string) => {
        // TODO: Реализовать удаление из БД
        await database.deleteNote(id);
        return id;
    }
);

interface NotesState {
    items: GeoNote[];
    loading: boolean;
    error: string | null;
}

const initialState: NotesState = {
    items: [],
    loading: false,
    error: null
};

const notesSlice = createSlice({
    name: 'notes',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            // loadNotes
            .addCase(loadNotes.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loadNotes.fulfilled, (state, action: PayloadAction<GeoNote[]>) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(loadNotes.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to load notes';
            })
            
            // TODO: Добавить обработчики для saveNote
            .addCase(saveNote.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(saveNote.fulfilled, (state, action: PayloadAction<GeoNote>) => {
                state.loading = false;
                state.items.push(action.payload);
                state.items.sort((a, b) => b.createdAt - a.createdAt);
            })
            .addCase(saveNote.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to save note';
            })
            
            // TODO: Добавить обработчики для removeNote
            .addCase(removeNote.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(removeNote.fulfilled, (state, action: PayloadAction<string>) => {
                state.loading = false;
                state.items = state.items.filter(note => note.id !== action.payload);
            })
            .addCase(removeNote.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to delete note';
            });
    }
});

export const { clearError } = notesSlice.actions;
export default notesSlice.reducer;