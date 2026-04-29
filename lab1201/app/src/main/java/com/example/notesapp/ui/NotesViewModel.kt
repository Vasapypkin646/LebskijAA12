package com.example.notesapp.ui

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.notesapp.data.Note
import com.example.notesapp.data.NoteRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class NotesViewModel(
    private val repository: NoteRepository
) : ViewModel() {

    private val _notes = MutableStateFlow<List<Note>>(emptyList())
    val notes: StateFlow<List<Note>> = _notes.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        loadNotes()
    }

    private fun loadNotes() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                repository.allNotes
                    .onEach { notesList ->
                        Log.d("NotesViewModel", "Received ${notesList.size} notes")
                        _notes.value = notesList
                        if (_isLoading.value) {
                            _isLoading.value = false
                        }
                    }
                    .launchIn(viewModelScope)
            } catch (e: Exception) {
                Log.e("NotesViewModel", "Error loading notes", e)
                _error.value = "Ошибка загрузки заметок"
                _isLoading.value = false
            }
        }
    }

    fun deleteNote(note: Note) {
        viewModelScope.launch {
            try {
                repository.deleteNote(note)
            } catch (e: Exception) {
                _error.value = "Ошибка удаления заметки"
            }
        }
    }

    fun clearError() {
        _error.value = null
    }
}