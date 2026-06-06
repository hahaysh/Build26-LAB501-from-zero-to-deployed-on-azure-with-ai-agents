import os
import math
import urllib.parse
import urllib.request
from flask import Flask, render_template, request, abort, Response, url_for
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cosmos DB configuration
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "LegoDatabase")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "legoSets")

if not COSMOS_ENDPOINT:
    raise RuntimeError(
        "COSMOS_ENDPOINT is not set. Copy src/.env.sample to src/.env and set "
        "COSMOS_ENDPOINT to your Cosmos DB account endpoint "
        "(e.g. https://<your-cosmos-account>.documents.azure.com:443/)."
    )

ITEMS_PER_PAGE = 24
SUPPORTED_LANGS = {"en", "ko"}
DEFAULT_UI_LANG = os.environ.get("UI_LANG", "ko").lower()

TRANSLATIONS = {
    "en": {
        "page_home": "Home",
        "page_browse": "Browse Sets",
        "page_not_found": "404 - Not Found",
        "nav_home": "Home",
        "nav_browse": "Browse",
        "nav_search_placeholder": "Search the galaxy...",
        "hero_intro": "A LONG TIME AGO IN A BRICK BOX FAR, FAR AWAY...",
        "hero_description": "Explore the ultimate collection of {total_sets} LEGO sets across {total_themes} themes. Search, discover, and relive the builds.",
        "hero_search_placeholder": "Search for any LEGO set...",
        "hero_search_button": "SEARCH",
        "stat_total_sets": "Total Sets",
        "stat_themes": "Themes",
        "stat_years": "Years of LEGO",
        "featured_heading": "LEGENDARY BUILDS",
        "featured_browse_all": "BROWSE ALL SETS",
        "browse_heading": "BROWSE SETS",
        "browse_showing_results": "Showing results for",
        "browse_in_theme": "in",
        "browse_sets_found": "{count} sets found",
        "browse_search_label": "Search",
        "browse_search_placeholder": "Set name...",
        "browse_theme_label": "Theme",
        "browse_all_themes": "All Themes",
        "browse_year_label": "Year",
        "browse_year_placeholder": "e.g. 2023",
        "browse_sort_label": "Sort",
        "browse_sort_name": "Name A-Z",
        "browse_sort_year_desc": "Newest First",
        "browse_sort_year_asc": "Oldest First",
        "browse_sort_parts_desc": "Most Parts",
        "browse_sort_parts_asc": "Fewest Parts",
        "browse_go": "GO",
        "browse_active_filters": "Active filters:",
        "browse_clear_all": "Clear all",
        "browse_owned": "OWNED",
        "browse_pieces": "pieces",
        "browse_prev": "Prev",
        "browse_next": "Next",
        "browse_no_sets": "NO SETS FOUND",
        "browse_no_sets_copy": "These are not the bricks you're looking for...",
        "browse_clear_filters": "Clear Filters",
        "detail_in_collection": "IN YOUR COLLECTION",
        "detail_set_prefix": "SET",
        "detail_pieces": "Pieces",
        "detail_released": "Released",
        "detail_set_number": "Set Number",
        "detail_theme": "Theme",
        "detail_year_released": "Year Released",
        "detail_number_of_parts": "Number of Parts",
        "detail_type": "Type",
        "detail_more_theme": "More {theme}",
        "detail_all_from_year": "All from {year}",
        "detail_more_from_theme": "MORE FROM {theme}",
        "not_found_heading": "DISTURBANCE IN THE FORCE",
        "not_found_copy": "The set you're looking for has been lost in hyperspace.",
        "not_found_subcopy": "It may have been moved, removed, or perhaps it existed only in a galaxy far, far away.",
        "not_found_home": "RETURN HOME",
        "not_found_search": "SEARCH SETS",
        "footer_tagline": "A long time ago in a brick box far, far away...",
        "footer_powered": "Powered by Azure Cosmos DB",
        "footer_sets_indexed": "{count} sets indexed",
        "lang_en": "EN",
        "lang_ko": "KR",
    },
    "ko": {
        "page_home": "홈",
        "page_browse": "세트 찾아보기",
        "page_not_found": "404 - 페이지를 찾을 수 없음",
        "nav_home": "홈",
        "nav_browse": "찾아보기",
        "nav_search_placeholder": "레고 세트를 검색하세요...",
        "hero_intro": "아주 오래전, 머나먼 브릭 박스에서...",
        "hero_description": "총 {total_sets}개의 LEGO 세트와 {total_themes}개의 테마를 탐색해 보세요. 검색하고, 발견하고, 다시 빌드의 즐거움을 떠올려 보세요.",
        "hero_search_placeholder": "원하는 LEGO 세트를 검색하세요...",
        "hero_search_button": "검색",
        "stat_total_sets": "전체 세트",
        "stat_themes": "테마 수",
        "stat_years": "레고 역사",
        "featured_heading": "대표 빌드",
        "featured_browse_all": "전체 세트 보기",
        "browse_heading": "세트 찾아보기",
        "browse_showing_results": "검색어",
        "browse_in_theme": "테마",
        "browse_sets_found": "{count}개 검색됨",
        "browse_search_label": "검색",
        "browse_search_placeholder": "세트 이름...",
        "browse_theme_label": "테마",
        "browse_all_themes": "모든 테마",
        "browse_year_label": "연도",
        "browse_year_placeholder": "예: 2023",
        "browse_sort_label": "정렬",
        "browse_sort_name": "이름순",
        "browse_sort_year_desc": "최신순",
        "browse_sort_year_asc": "오래된순",
        "browse_sort_parts_desc": "부품 많은순",
        "browse_sort_parts_asc": "부품 적은순",
        "browse_go": "이동",
        "browse_active_filters": "활성 필터:",
        "browse_clear_all": "모두 지우기",
        "browse_owned": "보유",
        "browse_pieces": "피스",
        "browse_prev": "이전",
        "browse_next": "다음",
        "browse_no_sets": "검색 결과 없음",
        "browse_no_sets_copy": "조건에 맞는 브릭을 찾지 못했습니다...",
        "browse_clear_filters": "필터 초기화",
        "detail_in_collection": "보유 중",
        "detail_set_prefix": "세트",
        "detail_pieces": "피스 수",
        "detail_released": "출시연도",
        "detail_set_number": "세트 번호",
        "detail_theme": "테마",
        "detail_year_released": "출시연도",
        "detail_number_of_parts": "부품 수",
        "detail_type": "유형",
        "detail_more_theme": "{theme} 더 보기",
        "detail_all_from_year": "{year}년 전체 보기",
        "detail_more_from_theme": "{theme}의 다른 세트",
        "not_found_heading": "포스를 흔드는 오류",
        "not_found_copy": "찾으시는 세트가 하이퍼스페이스에서 사라졌습니다.",
        "not_found_subcopy": "이동되었거나 삭제되었을 수 있고, 아주 먼 은하계에만 존재했을지도 모릅니다.",
        "not_found_home": "홈으로 이동",
        "not_found_search": "세트 검색",
        "footer_tagline": "아주 오래전, 머나먼 브릭 박스에서...",
        "footer_powered": "Azure Cosmos DB 기반",
        "footer_sets_indexed": "총 {count}개 세트 인덱싱",
        "lang_en": "EN",
        "lang_ko": "KR",
    },
}


def get_ui_lang():
    requested_lang = request.args.get("lang", "").lower()
    if requested_lang in SUPPORTED_LANGS:
        return requested_lang
    if DEFAULT_UI_LANG in SUPPORTED_LANGS:
        return DEFAULT_UI_LANG
    return "en"


@app.context_processor
def inject_ui_helpers():
    current_lang = get_ui_lang()

    def t(key, **kwargs):
        template = TRANSLATIONS.get(current_lang, {}).get(key)
        if template is None:
            template = TRANSLATIONS["en"].get(key, key)
        return template.format(**kwargs) if kwargs else template

    def localized_url(endpoint, **values):
        if current_lang != "en" and "lang" not in values:
            values["lang"] = current_lang
        return url_for(endpoint, **values)

    def switch_lang_url(target_lang):
        endpoint = request.endpoint or "home"
        values = dict(request.view_args or {})
        values.update(request.args.to_dict(flat=True))
        if target_lang == "en":
            values.pop("lang", None)
        else:
            values["lang"] = target_lang
        return url_for(endpoint, **values)

    return {
        "current_lang": current_lang,
        "t": t,
        "localized_url": localized_url,
        "switch_lang_url": switch_lang_url,
    }


def get_container():
    client_id = os.environ.get("AZURE_CLIENT_ID")
    if client_id:
        credential = ManagedIdentityCredential(client_id=client_id)
    else:
        credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
    database = client.get_database_client(COSMOS_DATABASE)
    return database.get_container_client(COSMOS_CONTAINER)


def query_cosmos(query, parameters=None, max_count=None):
    container = get_container()
    kwargs = {
        "query": query,
        "enable_cross_partition_query": True,
    }
    if parameters:
        kwargs["parameters"] = parameters
    if max_count:
        kwargs["max_item_count"] = max_count
    return list(container.query_items(**kwargs))


@app.route("/")
def home():
    # Featured sets — large popular sets
    featured = query_cosmos(
        "SELECT TOP 8 * FROM c WHERE c.number_of_parts > 2000 ORDER BY c.number_of_parts DESC"
    )
    # Stats
    stats = query_cosmos("SELECT VALUE COUNT(1) FROM c")
    total_sets = stats[0] if stats else 0
    theme_count = query_cosmos("SELECT VALUE COUNT(1) FROM (SELECT DISTINCT c.theme_name FROM c)")
    total_themes = theme_count[0] if theme_count else 0
    return render_template("home.html", featured=featured, total_sets=total_sets, total_themes=total_themes)


@app.route("/browse")
def browse():
    search = request.args.get("q", "").strip()
    theme = request.args.get("theme", "").strip()
    year = request.args.get("year", "").strip()
    sort = request.args.get("sort", "name")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    # Build query
    conditions = []
    parameters = []

    if search:
        conditions.append("CONTAINS(LOWER(c.name), LOWER(@search))")
        parameters.append({"name": "@search", "value": search})
    if theme:
        conditions.append("c.theme_name = @theme")
        parameters.append({"name": "@theme", "value": theme})
    if year:
        conditions.append("c.year_released = @year")
        parameters.append({"name": "@year", "value": int(year)})

    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Sort mapping
    sort_map = {
        "name": "c.name ASC",
        "year_desc": "c.year_released DESC",
        "year_asc": "c.year_released ASC",
        "parts_desc": "c.number_of_parts DESC",
        "parts_asc": "c.number_of_parts ASC",
    }
    order_by = sort_map.get(sort, "c.name ASC")

    # Count query
    count_query = f"SELECT VALUE COUNT(1) FROM c {where_clause}"
    count_result = query_cosmos(count_query, parameters or None)
    total_items = count_result[0] if count_result else 0
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * ITEMS_PER_PAGE
    data_query = f"SELECT * FROM c {where_clause} ORDER BY {order_by} OFFSET {offset} LIMIT {ITEMS_PER_PAGE}"
    sets = query_cosmos(data_query, parameters or None)

    # Get all themes for the filter dropdown
    themes = query_cosmos("SELECT DISTINCT VALUE c.theme_name FROM c ORDER BY c.theme_name ASC")

    return render_template(
        "browse.html",
        sets=sets,
        themes=themes,
        search=search,
        selected_theme=theme,
        selected_year=year,
        sort=sort,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
    )


@app.route("/set/<set_id>")
def detail(set_id):
    results = query_cosmos(
        "SELECT * FROM c WHERE c.id = @id",
        parameters=[{"name": "@id", "value": set_id}],
    )
    if not results:
        abort(404)
    lego_set = results[0]

    # Get related sets from the same theme
    related = query_cosmos(
        "SELECT TOP 6 * FROM c WHERE c.theme_name = @theme AND c.id != @id ORDER BY c.number_of_parts DESC",
        parameters=[
            {"name": "@theme", "value": lego_set["theme_name"]},
            {"name": "@id", "value": set_id},
        ],
    )
    return render_template("detail.html", set=lego_set, related=related)


@app.route("/image-proxy")
def image_proxy():
    """Proxy remote images (e.g. cdn.rebrickable.com) that are blocked from
    direct browser access in some lab/network environments."""
    url = request.args.get("url", "").strip()
    if not url or not url.startswith(("http://", "https://")):
        abort(400)
    # Only allow proxying from the rebrickable CDN to avoid an open proxy.
    allowed_hosts = ("cdn.rebrickable.com",)
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        abort(400)
    if parsed.hostname not in allowed_hosts:
        abort(403)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lego-vault-proxy/1.0"})
        with urllib.request.urlopen(req, timeout=10) as upstream:
            data = upstream.read()
            content_type = upstream.headers.get("Content-Type", "image/jpeg")
    except Exception:
        abort(502)

    return Response(data, content_type=content_type, headers={"Cache-Control": "public, max-age=86400"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
