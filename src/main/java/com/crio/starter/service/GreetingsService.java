package com.crio.starter.service;

import com.crio.starter.data.GreetingsEntity;

import com.crio.starter.repository.GreetingsRepository;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class GreetingsService {

  @Autowired
  private final GreetingsRepository greetingsRepository;

  public List<GreetingsEntity> getMemes(PageRequest pageRequest) {
    return greetingsRepository.findAll(pageRequest).getContent();
  }

  public Optional<GreetingsEntity> getMemeById(String id) {
    Optional<GreetingsEntity> meme = greetingsRepository.findById(id);
    return meme;
  }

  public String createMeme(GreetingsEntity meme) {
    GreetingsEntity savedMeme = greetingsRepository.save(meme);
    return savedMeme.getId();
  }

  public Optional<GreetingsEntity> getMemeByNameUrlAndCaption(@NonNull String name,
      @NonNull String url, @NonNull String caption) {
        return greetingsRepository.findByNameAndUrlAndCaption(name, url, caption);
  }


}