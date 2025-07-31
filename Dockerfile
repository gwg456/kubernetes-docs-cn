FROM ruby:3.1-alpine

# 安装依赖包
RUN apk add --no-cache \
    build-base \
    git \
    nodejs \
    npm

# 设置工作目录
WORKDIR /srv/jekyll

# 复制 Gemfile 和 Gemfile.lock
COPY Gemfile Gemfile.lock ./

# 安装 Ruby gems
RUN bundle install

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 4000

# 设置默认命令
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--livereload"]