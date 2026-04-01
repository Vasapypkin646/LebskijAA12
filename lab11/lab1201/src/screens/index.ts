// Экспортируем экраны
export { default as NotesListScreen } from './NotesListScreen';
export { default as AddNoteScreen } from './AddNoteScreen';

// NoteDetailScreen будет автоматически выбран в зависимости от платформы
// .native.tsx для Android/iOS, .web.tsx для веба
export { default as NoteDetailScreen } from './NoteDetailScreen';
