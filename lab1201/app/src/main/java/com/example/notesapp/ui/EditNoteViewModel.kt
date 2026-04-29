package com.example.notesapp.ui

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.notesapp.data.Note
import com.example.notesapp.data.NoteRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class EditNoteViewModel(
    private val repository: NoteRepository,
    private val noteId: Int,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _note = MutableStateFlow<Note?>(null)
    val note: StateFlow<Note?> = _note.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        loadNote()
    }

    private fun loadNote() {
        if (noteId > 0) {
            viewModelScope.launch {
                _isLoading.value = true
                try {
                    val loadedNote = repository.getNoteById(noteId)
                    _note.value = loadedNote
                } catch (e: Exception) {
                    _error.value = "Ошибка загрузки заметки"
                } finally {
                    _isLoading.value = false
                }
            }
        } else {
            _isLoading.value = false
        }
    }

    fun saveNote(title: String, content: String, onComplete: () -> Unit) {
        viewModelScope.launch {
            try {
                if (noteId > 0) {
                    val existingNote = _note.value
                    if (existingNote != null) {
                        val updatedNote = existingNote.copy(title = title, content = content)
                        repository.updateNote(updatedNote)
                    }
                } else {
                    val newNote = Note(title = title, content = content, createdAt = System.currentTimeMillis())
                    repository.insertNote(newNote)
                }
                onComplete()
            } catch (e: Exception) {
                _error.value = "Ошибка сохранения"
            }
        }
    }

    fun clearError() {
        _error.value = null
    }
}